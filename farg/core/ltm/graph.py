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

kLogger = logging.getLogger("LTM_topology")


class LTMGraph2(object):
  """Represents a graph to be stored in the long-term memory.

  Keyword Args:
    filename: If present, loads data from file. master_graph must not be present.
    master_graph: If present, copies data from master graph. filename must not be present.
    
  Attributes:
    nodes: A list of :py:class:`~farg.core.ltm.node.LTMNode` objects.
    content_to_nodes: A dictionary mapping content (each an instance of :py:class:`~farg.core.ltm.storable.LTMStorableMixin`)
      to nodes.
    is_working_copy: Boolean. When true, this is a working copy. Else a master copy to be saved to disk.
    filename: When not a working copy, contains filename where file is stored on disk.
    master_graph: When working copy, points to master graph.

  This contains nodes and edges.

  **Nodes**
  
  Nodes are instances of :py:class:`~farg.core.ltm.node.LTMNode`. A node has the attribute .content,
  (which is the concept being stored in the node, the very reason for the existence of the node), as
  well as other metadata such as activation level.

  The content of a node is a python object subclassing from :py:class:`~farg.core.ltm.storable.LTMStorableMixin`.
  A particular instance may depend for its definition on content of other graph nodes.

  **Storing to and retrieving from disk**
  
  Graphs can be stored on disk and retrieved. Given arbitrary dependencies between nodes, we rely on
  :py:mod:`pickle` to do the heavy-duty lifting of serialization and deserialization.
  
  There are two main ways to construct this graph: it can be loaded from a file, or it can be copied
  from another graph.
  
  In a given run, a graph is loaded from disk (let's call this graph O), and a copy made from it
  (Graph W). Graph W is the working copy which the app can update, and at the end, some salient
  items will make their way back to O, and it will be written to disk.
  
  The class LTM Manager handles this workflow. 
  """

  def __init__(self, *, filename=None, master_graph=None):
    self.nodes = []
    self.content_to_nodes = {}

    if filename:
      assert(not master_graph)
      self.is_working_copy = False
      self.filename = filename
      self._LoadFromFile()
    elif master_graph:
      assert(not filename)
      self.is_working_copy = True
      self.master_graph = master_graph
      self._CopyFromMaster()
    else:
      raise FargError("One of filename or master_graph needs to be passed in")

      
  def GetNodes(self):
    """Returns list of nodes. Don't modify this list."""
    return self.nodes

  def IsEmpty(self):
    """True if there are no nodes."""
    return not self.nodes

  def DumpToFile(self):
    """Writes out content to file (if not working copy)."""
    assert(not self.is_working_copy)

    with open(self.filename, "wb") as ltm_file:
      pickler = pickle.Pickler(ltm_file, 2)
      for node in self.nodes:
        self._Mangle(node.content.__dict__)
        pickler.dump(node)
        self._Unmangle(node.content.__dict__)
  
  # TODO: rename to GetNode(self, *, content)
  def GetNode(self, *, content):
    """Returns node for content; creates one if it does not exist."""
    storable_content = content.GetLTMStorableContent()
    if storable_content in self._content_to_node:
      return self._content_to_node[storable_content]

    new_node = LTMNode(storable_content)
    self.nodes.append(new_node)
    self._content_to_node[storable_content] = new_node
    # Also ensure presence of any dependent nodes.
    for dependent_content in storable_content.LTMDependentContent():
      self.GetNode(content=dependent_content)
    return new_node


  def _LoadFromFile(self):
    """Loads graph nodes from file.
    
    The file contains pickled nodes, and dependent data has been replaced with nodes. All this
    needs to be undone to load from file."""
    with open(self.filename, "rb") as ltmfile:
      unpickler = pickle.Unpickler(ltmfile)
      while True:
        try:
          node = unpickler.load()
          self._AddNode(node)
        except EOFError:
          break
        except ValueError:
          # Hit in Py3 for empty input file...
          break

  def _CopyFromMaster(self):
    """Copies nodes from master."""
    for node in self.master_graph.GetNodes():
      self._AddNodeCopy(node)
  
  def _AddNode(self, node):
    """Adds node to graph."""
    assert(isinstance(node, LTMNode))
    if not node.content in self._content_to_node:
      self._content_to_node[node.content] = node
      self.nodes.append(node)

  def _AddNodeCopy(self, node):
    """Adds a copy of node to graph."""
    assert(isinstance(node, LTMNode))
    node_copy = LTMNode(content=node.content)
    self._AddNode(node_copy)

  def _Mangle(self, content_dict):
    """Replaces references to node contents with the nodes themselves."""
    for k, value in content_dict.items():
      if value in self._content_to_node:
        content_dict[k] = self._content_to_node[value]

  def _Unmangle(self, content_dict):
    """Replaces values that are nodes with contents of those nodes."""
    for k, value in content_dict.items():
      if isinstance(value, LTMNode):
        content_dict[k] = value.content

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
      kLogger.info("Added LTM node %s", node.content)

  def GetNode(self, *, content):
    """Returns node for content; creates one if it does not exist."""
    storable_content = content.GetLTMStorableContent()
    if storable_content in self._content_to_node:
      return self._content_to_node[storable_content]
    logging.debug("Created new LTM node [%s]", storable_content)
    new_node = LTMNode(storable_content)
    self.nodes.append(new_node)
    self._content_to_node[storable_content] = new_node
    # Also ensure presence of any dependent nodes.
    for dependent_content in storable_content.LTMDependentContent():
      self.GetNode(content=dependent_content)
    return new_node

  def AddEdgeBetweenContent(self, from_content, to_content,
                            edge_type=LTMEdge.LTM_EDGE_TYPE_RELATED):
    node = self.GetNode(content=from_content.GetLTMStorableContent())
    to_node = self.GetNode(content=to_content.GetLTMStorableContent())
    for edge in node.outgoing_edges:
      if edge.to_node == to_node:
        if edge_type != edge.edge_type:
          raise FargError("Edge already exists, but with diff type!")
        # Already exists, bail out.
        return
    node.outgoing_edges.append(LTMEdge(to_node, edge_type))

  def IsContentSufficientlyActive(self, content, *, threshold=0.8):
    activation = self.GetNode(content=content).GetActivation(current_time=self._timesteps)
    return activation >= threshold
