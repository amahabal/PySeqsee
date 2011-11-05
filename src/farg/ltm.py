"""Long term memory."""

import cPickle as pickle

class LTMNode(object):
  """Represents a node in the graph of LTM.
  
  Each node has a content --- an instance of some python class that implements Caching by using a
  Create() method where the following is guarenteed for any instance inst:

  inst == inst.__class__.Create(**inst.__dict__)
  """

  def __init__(self, content):
    self.content = content

  def __getstate__(self):
    content = self.content
    return (content.__class__, content.__dict__)

  def __setstate__(self, state):
    clsname, instance_dict = state
    LTM.Unmangle(instance_dict)
    self.content = clsname.Create(**instance_dict)

class LTM(object):
  def __init__(self, nodes_filename, edges_filename):
    self.nodes = []
    self.edges = []
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
    for k, v in content_dict.iteritems():
      if isinstance(v, LTMNode):
        content_dict[k] = v.content

  def LoadNodes(self, unpickler):
    while True:
      try:
        node = unpickler.load()
        print "Loaded node content=", node.content
        self.AddNode(node)
      except EOFError:
        print "Done reading"
        break
    for node in self.nodes:
      LTM.Unmangle(node.content.__dict__)


  def LoadEdges(self, unpickler):
    while True:
      try:
        edge = unpickler.load()
        self.AddEdge(edge)
      except EOFError:
        print "Done reading"
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
    self.nodes.append(node)

  def AddEdge(self, edge):
    self.edges.append(edge)
