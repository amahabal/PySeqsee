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
from farg.core.ltm.node import LTMNode, Unmangle
import logging
import pickle as pickle

kLogger = logging.getLogger("LTM_topology")


class LTMGraph(object):
  """Represents a graph to be stored in the long-term memory.

  Keyword Args:
    filename: If present, loads data from file. master_graph must not be present.
    master_graph: If present, copies data from master graph. filename must not be present.

  Attributes:
    nodes: A list of :py:class:`~farg.core.ltm.node.LTMNode` objects.
    _content_to_node: A dictionary mapping content (each an instance of :py:class:`~farg.core.ltm.storable.LTMStorableMixin`)
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

  def __init__(self, *, filename=None, master_graph=None, empty_ok_for_test=False):
    self.nodes = []
    self._content_to_node = {}

    if filename:
      assert(not master_graph)
      self.is_working_copy = False
      self.transient_ltm = False
      self.filename = filename
      self._LoadFromFile()
    elif master_graph:
      assert(not filename)
      self.is_working_copy = True
      self.master_graph = master_graph
      self.transient_ltm = False
      self._LoadFromFile()
    elif empty_ok_for_test:
      self.transient_ltm = True
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
    if self.transient_ltm:
      return
    assert(not self.is_working_copy)

    with open(self.filename, "wb") as ltm_file:
      pickler = pickle.Pickler(ltm_file, 2)
      for node in self.nodes:
        self._Mangle(node.content.__dict__)
        pickler.dump(node)
        Unmangle(node.content.__dict__)

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
      # Add an edge indicating dependence.
      self.AddEdge(content, dependent_content, edge_type_set={LTMEdge.LTM_EDGE_TYPE_DEP_ON})
    return new_node

  def UploadToMaster(self, *, threshold=0.05):
    if self.transient_ltm:
      return
    mg = self.master_graph
    kept_nodes = set()
    for n in self.nodes:
      if n.GetActivation(0) > threshold:
        kept_nodes.add(n)
        # print('Keeping: %5.3f %s' % (n.GetActivation(0), n.content.BriefLabel()))
        mg._IncrementAbundance(content=n.content)
    for n in self.nodes:
      if not n in kept_nodes:
        continue
      for e in n.GetOutgoingEdges():
        target = e.to_node
        if not target in kept_nodes:
          continue
        mg.StrengthenEdge(n.content, target.content, edge_type_set=e.edge_type_set)
        # print("Strengthening %s --> %s" % (n.content.BriefLabel(), target.content.BriefLabel()))

  def _IncrementAbundance(self, *, content):
    """Increments abundance by 1."""
    self.GetNode(content=content).abundance += 1

  def _LoadFromFile(self):
    """Loads graph nodes from file.

    The file contains pickled nodes, and dependent data has been replaced with nodes. All this
    needs to be undone to load from file."""
    if hasattr(self, 'filename'):
      filename = self.filename
    else:
      filename = self.master_graph.filename
    with open(filename, "rb") as ltmfile:
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

  def _AddNode(self, node):
    """Adds node to graph."""
    assert(isinstance(node, LTMNode))
    if not node.content in self._content_to_node:
      self._content_to_node[node.content] = node
      self.nodes.append(node)

  def _Mangle(self, content_dict):
    """Replaces references to node contents with the nodes themselves."""
    for k, value in content_dict.items():
      if isinstance(value, tuple):
        content_dict[k] = self._MangleTuple(value)
      elif value in self._content_to_node:
        content_dict[k] = self._content_to_node[value]

  def _MangleTuple(self, value):
    out = []
    for k in value:
      if isinstance(k, tuple):
        out.append(self._MangleTuple(k))
      elif k in self._content_to_node:
        out.append(self._content_to_node[k])
      else:
        out.append(k)
    return tuple(out)

  def AddEdge(self, from_content, to_content, *, utility=1, edge_type_set=set()):
    node = self.GetNode(content=from_content.GetLTMStorableContent())
    to_node = self.GetNode(content=to_content.GetLTMStorableContent())
    for edge in node.outgoing_edges:
      if edge.to_node == to_node:
        edge.edge_type_set.update(edge_type_set)
        # Already exists.
        return
    node.outgoing_edges.append(LTMEdge(to_node, edge_type_set=edge_type_set.copy(), utility=utility))

  def StrengthenEdge(self, from_content, to_content, *,
                     edge_type_set=set()):
    node = self.GetNode(content=from_content.GetLTMStorableContent())
    to_node = self.GetNode(content=to_content.GetLTMStorableContent())
    for edge in node.outgoing_edges:
      if edge.to_node == to_node:
        edge.utility += 1
        if edge_type_set:
          edge.edge_type_set.update(edge_type_set)
        return
    node.outgoing_edges.append(LTMEdge(to_node, edge_type_set=edge_type_set.copy(), utility=1))
