# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

from farg.core.exceptions import FargError
from farg.core.ltm.edge import LTMEdge
from farg.core.ltm.node import LTMNode
import logging
import pickle as pickle

logger = logging.getLogger(__name__)

class LTMGraph(object):
  """Represents a full LTM graph (consisting of nodes and edges)."""
  def __init__(self, filename=None):
    """Initialization loads up the nodes and edges of the graph."""
    #: Nodes in the graph. Each is a LTMNode.
    self.nodes = []
    #: A utility data-structure mapping content to nodes. A particular piece of content
    #: should have at most one node.
    self._content_to_node = {}
    #: The filename for reading the graph from and for dumping the graph to.
    #: Must exist if we want to persist the LTM, but may be empty for testing.
    #: .. todo:: we need to be able to create this if missing.
    self._filename = filename
    #: Elapsed time-steps. Activation is time dependent since it decays at each time step. A
    #: notion of time is therefore relevant.
    self._timesteps = 0
    if filename:
      with open(filename, "rb") as ltmfile:
        up = pickle.Unpickler(ltmfile)
        self._LoadNodes(up)
    logging.info('Loaded LTM in %s: %d nodes read', filename, len(self.nodes))

  def _LoadNodes(self, unpickler):
    """Load all nodes from the unpickler.
    
    Each thing unpickled is a LTMNode. Because that class defines a __setstate__, it is used 
    to setup the state of the created node.
    
    While pickling, the content of that node (in a mangled state, see below) and its class is
    stored. When unpickling (this method), __setstate__ of LTMNode calls Create on this class
    (defined in LTMStorableMixin), and it ensures a proper non-duplicate initialization.
    """
    while True:
      try:
        node = unpickler.load()
        self.AddNode(node)
      except EOFError:
        break
      except ValueError:
        # Hit in Py3 for empty input file...
        break

  def IsEmpty(self):
    """True if there are zero-nodes."""
    return not self.nodes

  def Dump(self):
    """Writes out content to file if file attribute is set."""
    if not self._filename:
      return
    with open(self._filename, "wb") as ltm_file:
      pickler = pickle.Pickler(ltm_file, 2)
      for node in self.nodes:
        self._Mangle(node.content.__dict__)
        pickler.dump(node)
        self._Unmangle(node.content.__dict__)

  def _Mangle(self, content_dict):
    """Replaces references to nodes with the nodes themselves."""
    for k, value in content_dict.items():
      if value in self._content_to_node:
        content_dict[k] = self._content_to_node[value]

  def _Unmangle(self, content_dict):
    """Replaces values that are nodes with contents of those nodes."""
    for k, value in content_dict.items():
      if isinstance(value, LTMNode):
        content_dict[k] = value.content


  def AddNode(self, node):
    assert(isinstance(node, LTMNode))
    if not node.content in self._content_to_node:
      self._content_to_node[node.content] = node
      self.nodes.append(node)

  def GetNodeForContent(self, content):
    """Returns node for content; creates one if it does not exist."""
    storable_content = content.GetLTMStorableContent()
    if storable_content in self._content_to_node:
      return self._content_to_node[storable_content]
    new_node = LTMNode(storable_content)
    self.nodes.append(new_node)
    self._content_to_node[storable_content] = new_node
    # Also ensure presence of any dependent nodes.
    for dependent_content in storable_content.LTMDependentContent():
      self.GetNodeForContent(dependent_content)
    return new_node

  def SpikeForContent(self, content, amount):
    """Spike node indicated by content by amount."""
    storable_content = content.GetLTMStorableContent()
    self.GetNodeForContent(storable_content).Spike(amount, self._timesteps)

  def AddEdgeBetweenContent(self, from_content, to_content,
                            edge_type=LTMEdge.LTM_EDGE_TYPE_RELATED):
    node = self.GetNodeForContent(from_content.GetLTMStorableContent())
    to_node = self.GetNodeForContent(to_content.GetLTMStorableContent())
    for edge in node.outgoing_edges:
      if edge.to_node == to_node:
        if edge_type != edge.edge_type:
          raise FargError("Edge already exists, but with diff type!")
        # Already exists, bail out.
        return
    node.outgoing_edges.append(LTMEdge(to_node, edge_type))

  def GetGraphXDOT(self):
    """Generates XDOT for entire graph."""
    lines = []
    node_to_pos = dict((y, x) for x, y in enumerate(self.nodes))
    for node in self.nodes:
      lines.append(node.GetXDot(node_to_pos[node]))
      for edge in node.outgoing_edges:
        other_node = edge.to_node
        try:
          lines.append('node_%d -> node_%d' % (node_to_pos[node], node_to_pos[other_node]))
        except KeyError:
          print("Key error: %s  ==> %s" % (node.content.BriefLabel(),
                                           other_node.content.BriefLabel(),
                                           edge.edge_type))
          print((node, other_node))
          print(self.nodes)
    return """
      digraph G {
      %s
      }
      """ % ('\n'.join(lines))

  def GetGraphAroundNodeXDot(self, node_position, depth=3):
    """Get XDot of node outward from given node position upto given depth."""
    nodes = self.nodes
    node_to_pos = dict((y, x) for x, y in enumerate(self.nodes))
    lines = [nodes[node_position].GetXDot(node_position)]
    nodes_to_depth = { node_position: 0 }
    nodes_at_depth = [[node_position]]
    for depth in range(1, depth):
      nodes_at_this_depth = []
      for node_at_previous_depth in nodes_at_depth[depth - 1]:
        edges = nodes[node_at_previous_depth].outgoing_edges
        for edge in edges:
          other_node = node_to_pos[edge.to_node]
          if other_node not in nodes_to_depth:
            nodes_to_depth[other_node] = depth
            nodes_at_this_depth.append(other_node)
            lines.append(nodes[other_node].GetXDot(other_node))
          lines.append('node_%d -> node_%d;' % (node_at_previous_depth, other_node))
      nodes_at_depth.append(nodes_at_this_depth)
    # For the "leaf" nodes, add edges (without adding nodes)
    for node_at_previous_depth in nodes_at_depth[depth]:
      edges = nodes[node_at_previous_depth].outgoing_edges
      for edge in edges:
        other_node = node_to_pos[edge.to_node]
        if other_node in nodes_to_depth:
          lines.append('node_%d -> node_%d;' % (node_at_previous_depth, other_node))
    return """
      digraph G {
      %s
      }
      """ % ('\n'.join(lines))
