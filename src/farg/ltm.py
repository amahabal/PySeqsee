"""Long term memory."""

import cPickle as pickle

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

class LTMNode(object):
  """Represents a node in the graph of LTM.
  
  Each node has a content --- an instance of some python class that implements Caching by using a
  Create() method where the following is guarenteed for any instance inst::

    inst == inst.__class__.Create(**inst.__dict__)
  """

  def __init__(self, content):
    self.content = content
    self.outgoing_edges = []

  def GetOutgoingEdges(self):
    return self.outgoing_edges

  def __getstate__(self):
    """This saves the class name of content and (mangled) __dict__, to be reconstructed
    using Create().
    
    Mangling consists of replacing any value with the node of which that value is the content.
    
    This is needed since we wish to pass everything we are reviving through Create() of appropriate
    classes, and pickle has its own ideas of how to recreate. I wish to limit complexity to this
    class (rather than spreading to many), hence modifying how other classes get pickled is not
    an option.
    """
    content = self.content
    return (content.__class__, content.__dict__, self.outgoing_edges)

  def __setstate__(self, state):
    """This vivifies the object, using Create() and unmangling any values: that is, values that are
    nodes are replaced by their contents."""
    clsname, instance_dict, outgoing_edges = state
    LTM.Unmangle(instance_dict)
    self.content = clsname.Create(**instance_dict)
    self.outgoing_edges = outgoing_edges

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

  @staticmethod
  def Unmangle(content_dict):
    """Replaces values that are nodes with contents of those nodes."""
    for k, v in content_dict.iteritems():
      if isinstance(v, LTMNode):
        content_dict[k] = v.content

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
    self.GetNodeForContent(from_content).outgoing_edges.append(edge)
