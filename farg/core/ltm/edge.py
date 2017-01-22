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

     We store a number representing the utility of the edge, roughly implying how frequently that
     connection has been noted. We will also store a distribution of particular types of
     relationships seen (such as LTM_EDGE_TYPE_ISA).
  """

  #: Some predefined types of edges.
  LTM_EDGE_TYPE_ISA = "is_a"

  def __init__(self, to_node, *, edge_type_set, utility=1):
    #: Other end of the node.
    self.to_node = to_node
    #: Utility (an integer representing commonality.This will change).
    self.utility = utility
    #: Distribution of types.
    self.edge_type_set = set()
    if edge_type_set:
      self.edge_type_set = edge_type_set.copy()

