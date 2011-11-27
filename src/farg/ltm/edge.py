class LTMEdge(object):
  """Represents the connection between a pair of concepts.

  An edge is directed, and it is stored in the node for which this is an outgoing edge.
  """

  #: Some predefined types of edges.
  #: .. todo:: This needs to be extensible; currently a predefined set.
  LTM_EDGE_TYPE_RELATED = 1
  LTM_EDGE_TYPE_FOLLOWS = 2
  LTM_EDGE_TYPE_ISA = 3
  LTM_EDGE_CAN_BE_SEEN_AS = 4

  def __init__(self, to_node, edge_type):
    #: Other end of the node.
    self.to_node = to_node
    #: Type of the edge.
    self.edge_type = edge_type

