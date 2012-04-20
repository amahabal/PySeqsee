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

class LTMEdge(object):  # Has no public methods pylint:disable=R0903
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

