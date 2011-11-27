"""Long term memory."""

import cPickle as pickle
import math

from farg.ltm.node import LTMNode
from farg.ltm.edge import LTMEdge

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


class LTM(object):
  def __init__(self, filename):
    """Initialization loads up the nodes and edges of the graph."""
    self.nodes = []
    self.content_to_node = {}
    self.filename = filename
    with open(filename) as f:
      up = pickle.Unpickler(f)
      self.LoadNodes(up)

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

  def Dump(self):
    content_to_node_map = dict((x.content, x) for x in self.nodes)
    with open(self.filename, "w") as f:
      pickler = pickle.Pickler(f, 2)
      for node in self.nodes:
        LTM.Mangle(node.content.__dict__, content_to_node_map)
        pickler.dump(node)

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

  def AddEdgeBetweenContent(self, from_content, to_content, edge_type=LTMEdge.LTM_EDGE_TYPE_RELATED):
    edge = LTMEdge(self.GetNodeForContent(to_content), edge_type)
    self.GetNodeForContent(from_content)._outgoing_edges.append(edge)
