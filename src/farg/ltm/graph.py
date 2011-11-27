import cPickle as pickle
from farg.ltm.node import LTMNode
from farg.ltm.edge import LTMEdge

from farg.ltm_old import LTMStorableMixin

class LTMGraph(object):
  """Represents a full LTM graph (consisting of nodes and edges)."""
  def __init__(self, filename):
    """Initialization loads up the nodes and edges of the graph."""
    #: Nodes in the graph. Each is a LTMNode.
    self.nodes = []
    #: A utility data-structure mapping content to nodes. A particular piece of content should
    #: have at most one node.
    self.content_to_node = {}
    #: The filename for reading the graph from and for dumping the graph to. Must exist.
    #: .. todo:: we need to be able to create this if missing.
    self.filename = filename
    #: Elapsed time-steps. Activation is time dependent since it decays at each time step. A
    #: notion of time is therefore relevant.
    self.timesteps = 0
    with open(filename) as f:
      up = pickle.Unpickler(f)
      self.LoadNodes(up)

  def LoadNodes(self, unpickler):
    """Load all nodes from the unpickler.
    
    Each thing unpickled is a LTMNode. Because that class defines a __setstate__, it is used to
    setup the state of the created node.
    
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

  def Dump(self):
    with open(self.filename, "w") as f:
      pickler = pickle.Pickler(f, 2)
      for node in self.nodes:
        self.Mangle(node.content.__dict__)
        pickler.dump(node)

  def Mangle(self, content_dict):
    """Replaces references to nodes with the nodes themselves."""
    for k, v in content_dict.iteritems():
      if v in self.content_to_node:
        content_dict[k] = self.content_to_node[v]


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

