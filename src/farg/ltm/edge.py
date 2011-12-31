class LTMEdge(object):
  """Represents the connection between a pair of concepts.

     An edge is directed, and it is stored in the node for which this is an outgoing edge.
  """

  #: Some predefined types of edges.
  LTM_EDGE_TYPE_RELATED = "related"
  LTM_EDGE_TYPE_FOLLOWS = "follows"
  LTM_EDGE_TYPE_ISA = "is_a"
  LTM_EDGE_CAN_BE_SEEN_AS = "can_be_seen_as"

  def __init__(self, to_node, edge_type):
    #: Other end of the node.
    self.to_node = to_node
    #: Type of the edge.
    self.edge_type = edge_type

