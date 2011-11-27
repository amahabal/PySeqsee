"""Long term memory."""

import cPickle as pickle
import math

from farg.ltm.node import LTMNode

LTM_EDGE_TYPE_RELATED = 1
LTM_EDGE_TYPE_FOLLOWS = 2
LTM_EDGE_TYPE_ISA = 3
LTM_EDGE_CAN_BE_SEEN_AS = 4

class LTMStorableMixin(object):
  """Any class whose instances should be stored in LTM must adhere to certain semantics, and
  subclass from this class.
  
  For a given set of arguments, this class ensures that only a single object is created.
  """
  memos = {}

  @classmethod
  def Create(cls, **kwargs):
    key = frozenset(kwargs.items())
    if key not in cls.memos:
      new_instance = cls(**kwargs)
      cls.memos[key] = new_instance
      return new_instance
    return cls.memos[key]

  @classmethod
  def ClearMemos(cls):
    memos = {}

#: Maps raw activation (an integer) to real activation.
#: The values, in steps of 10, are as follows:
#: ['0.003', '0.018', '0.043', '0.093', # For 0, 10, 20, 30
#:  '0.220', '0.562', '0.811', '0.895', # For 40, 50, 60, 70
#:  '0.932', '0.952', '0.964']  # For 80, 90, 100
_raw_activation_to_real_activation = [
    0.4815 + 0.342 * math.atan2(12 * (0.01 * x - 0.5), 1)
    for x in range(2, 203)]


class LTMEdge(object):
  def __init__(self, to_node, edge_type):
    self.to_node = to_node
    self.edge_type = edge_type

class LTM(object):
  def __init__(self, nodes_filename, edges_filename):
    """Initialization loads up the nodes and edges of the graph."""
    self.nodes = []
    self.edges = []
    self.content_to_node = {}
    self.nodes_filename = nodes_filename
    self.edges_filename = edges_filename
    with open(nodes_filename) as f:
      up = pickle.Unpickler(f)
      self.LoadNodes(up)
    with open(edges_filename) as f:
      up = pickle.Unpickler(f)
      self.LoadEdges(up)

  @staticmethod
  def Mangle(content_dict, content_to_node_map):
    """Replaces references to nodes with the nodes themselves."""
    for k, v in content_dict.iteritems():
      if v in content_to_node_map:
        content_dict[k] = content_to_node_map[v]

  def LoadNodes(self, unpickler):
    while True:
      try:
        node = unpickler.load()
        self.AddNode(node)
      except EOFError:
        break


  def LoadEdges(self, unpickler):
    while True:
      try:
        edge = unpickler.load()
        self.AddEdge(edge)
      except EOFError:
        break

  def Dump(self):
    content_to_node_map = dict((x.content, x) for x in self.nodes)
    with open(self.nodes_filename, "w") as f:
      pickler = pickle.Pickler(f, 2)
      for node in self.nodes:
        LTM.Mangle(node.content.__dict__, content_to_node_map)
        pickler.dump(node)
    with open(self.edges_filename, "w") as f:
      pickler = pickle.Pickler(f, 2)
      for edge in self.edges:
        pickler.dump(edge)

  def AddNode(self, node):
    assert(isinstance(node, LTMNode))
    if not node.content in self.content_to_node:
      self.content_to_node[node.content] = node
      self.nodes.append(node)

  def GetNodeForContent(self, content):
    """Returns node for content; creates one if it does not exist."""
    assert(isinstance(content, LTMStorableMixin))
    if content in self.content_to_node:
      return self.content_to_node[content]
    new_node = LTMNode(content)
    self.nodes.append(new_node)
    self.content_to_node[content] = new_node
    return new_node

  def AddEdgeBetweenContent(self, from_content, to_content, edge_type=LTM_EDGE_TYPE_RELATED):
    edge = LTMEdge(self.GetNodeForContent(to_content), edge_type)
    self.GetNodeForContent(from_content)._outgoing_edges.append(edge)
