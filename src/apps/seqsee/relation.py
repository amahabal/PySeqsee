"""A relation is a specific instance of a mapping."""

from farg.focusable_mixin import FocusableMixin
from farg.codelet import Codelet

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
    from apps.seqsee.codelet_families.all import CF_GroupFromRelation
    if self.AreEndsContiguous():
      return (Codelet(CF_GroupFromRelation, controller, 50, relation=self),)
    else:
      return ()

  def GetSimilarityAffordances(self, focusable, other_fringe, my_fringe, controller):
    return ()


