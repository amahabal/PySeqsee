import cPickle as pickle
from farg.ltm.node import LTMNode
from farg.ltm.edge import LTMEdge

from farg.ltm.storable import LTMStorableMixin, LTMMakeStorableMixin

class LTMGraph(object):
  """Represents a full LTM graph (consisting of nodes and edges)."""
  def __init__(self, filename):
    """Initialization loads up the nodes and edges of the graph."""
    #: Nodes in the graph. Each is a LTMNode.
    self._nodes = []
    #: A utility data-structure mapping content to nodes. A particular piece of content should
    #: have at most one node.
    self._content_to_node = {}
    #: The filename for reading the graph from and for dumping the graph to. Must exist.
    #: .. todo:: we need to be able to create this if missing.
    self._filename = filename
    #: Elapsed time-steps. Activation is time dependent since it decays at each time step. A
    #: notion of time is therefore relevant.
    self._timesteps = 0
    with open(filename) as f:
      up = pickle.Unpickler(f)
      self._LoadNodes(up)

  def _LoadNodes(self, unpickler):
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
    with open(self._filename, "w") as f:
      pickler = pickle.Pickler(f, 2)
      for node in self._nodes:
        self._Mangle(node.content.__dict__)
        pickler.dump(node)
        self._Unmangle(node.content.__dict__)

  def _Mangle(self, content_dict):
    """Replaces references to nodes with the nodes themselves."""
    for k, v in content_dict.iteritems():
      if v in self._content_to_node:
        content_dict[k] = self._content_to_node[v]

  def _Unmangle(self, content_dict):
    """Replaces values that are nodes with contents of those nodes."""
    for k, v in content_dict.iteritems():
      if isinstance(v, LTMNode):
        content_dict[k] = v.content


  def AddNode(self, node):
    assert(isinstance(node, LTMNode))
    if not node.content in self._content_to_node:
      self._content_to_node[node.content] = node
      self._nodes.append(node)

  def GetNodeForContent(self, content):
    """Returns node for content; creates one if it does not exist."""
    if isinstance(content, LTMMakeStorableMixin):
      content = content.CreateLTMStorable(content)
    else:
      assert(isinstance(content, LTMStorableMixin))
    if content in self._content_to_node:
      return self._content_to_node[content]
    new_node = LTMNode(content)
    self._nodes.append(new_node)
    self._content_to_node[content] = new_node
    return new_node

  def AddEdgeBetweenContent(self, from_content, to_content, edge_type=LTMEdge.LTM_EDGE_TYPE_RELATED):
    edge = LTMEdge(self.GetNodeForContent(to_content), edge_type)
    self.GetNodeForContent(from_content)._outgoing_edges.append(edge)

