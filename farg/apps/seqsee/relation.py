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
from farg.apps.seqsee.distance import DistanceInElements

"""A relation is a specific instance of a mapping."""

from farg.core.codelet import Codelet
from farg.core.focusable_mixin import FocusableMixin

class Relation(FocusableMixin):
  def __init__(self, first, second, *, mapping_set):
    #: The object on the left.
    self.first = first
    #: The object on the right.
    self.second = second
    #: The set of mappings any of which transform the left object to the right object.
    self.mapping_set = mapping_set

  def __str__(self):
    return '%s-->%s (%s)' % (self.first, self.second, self.mapping_set)

  def Ends(self):
    """Returns a 2-tuple of the two ends."""
    return (self.first, self.second)

  def GetMappingSet(self):
    """Returns the set of mappings. Currently, this is a singleton, but in order to see
    relations between "2" and "3" flexibly as "next number" as well as "next prime", multiple
    relations will need to be supported.
    """
    return self.mapping_set

  def AreEndsContiguous(self):
    """Are the two ends right next to each other (i.e., true if no hole)."""
    return self.first.end_pos + 1 == self.second.start_pos

  def GetFringe(self, controller):
    return dict((controller.ltm.GetNodeForContent(x), 1.0) for x in self.mapping_set)

  def GetAffordances(self, controller):
    # TODO(# --- Jan 3, 2012): Too eager, tone this down later.
    from farg.apps.seqsee.codelet_families.all import CF_GroupFromRelation
    from farg.apps.seqsee.codelet_families.all import CF_IsThisInterlaced
    if self.AreEndsContiguous():
      return (Codelet(CF_GroupFromRelation, controller, 50, dict(relation=self)),)
    else:
      distance_in_elements = self.second.start_pos - self.first.end_pos - 1
      distance_object = DistanceInElements(value=distance_in_elements)
      if controller.ltm.IsContentSufficientlyActive(distance_object):
        return (Codelet(CF_IsThisInterlaced, controller, 50,
                        dict(distance=distance_object)),)
      else:
        return ()

  def GetSimilarityAffordances(self, focusable, other_fringe, my_fringe, controller):
    return ()

  def OnFocus(self, controller):
    """When the relation is focused on, and is not adjacent, send activation to the
       "distance" node.
    """
    if not self.AreEndsContiguous():
      distance_in_elements = self.second.start_pos - self.first.end_pos - 1
      distance_object = DistanceInElements(value=distance_in_elements)
      # TODO(# --- Apr 22, 2012): Need to do something for group distances, too.
      controller.ltm.IncreaseActivationForContent(distance_object, 5)

