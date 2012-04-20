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

"""A relation is a specific instance of a mapping."""

from farg.core.codelet import Codelet
from farg.core.focusable_mixin import FocusableMixin

class Relation(FocusableMixin):
  def __init__(self, first, second, mapping):
    #: The object on the left.
    self.first = first
    #: The object on the right.
    self.second = second
    #: The mapping to transform the left object to the right object.
    self.mapping = mapping

  def __str__(self):
    return '%s-->%s (%s)' % (self.first, self.second, self.mapping)

  def Ends(self):
    """Returns a 2-tuple of the two ends."""
    return (self.first, self.second)

  def AreEndsContiguous(self):
    """Are the two ends right next to each other (i.e., true if no hole)."""
    return self.first.end_pos + 1 == self.second.start_pos

  def GetFringe(self, controller):
    mapping_node = controller.ltm.GetNodeForContent(self.mapping)
    return {mapping_node: 1.0}

  def GetAffordances(self, controller):
    # TODO(# --- Jan 3, 2012): Too eager, tone this down later.
    from farg.apps.seqsee.codelet_families.all import CF_GroupFromRelation
    if self.AreEndsContiguous():
      return (Codelet(CF_GroupFromRelation, controller, 50, dict(relation=self)),)
    else:
      return ()

  def GetSimilarityAffordances(self, focusable, other_fringe, my_fringe, controller):
    return ()


