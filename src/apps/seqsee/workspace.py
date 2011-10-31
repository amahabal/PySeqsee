"""Workspace. Modeled after the workspace in the Perl version.

.. warning:: No attempt to optimize is being made. Later, with profiling, we can speed things up.

  Specifically, groups are being kept in a set, supergroups-related bookkeeping is not being
  maintained, and so forth. If profiling reveals these to be issues, these can later be optimized.
"""

from apps.seqsee.sobject import SAnchored, SElement, SGroup, SObject
from farg.exceptions import FargError, ConflictingGroupException
from apps.seqsee.util import LessThan, LessThanEq, GreaterThan, GreaterThanEq, Exactly

class Workspace(object):
  def __init__(self):
    #: All elements. Each is a :class:`~apps.seqsee.sobject.SAnchored` object.
    self.elements = []
    #: Number of elements.
    self.num_elements = 0
    #: Groups (excluding single element groups).
    #: Each is a :class:`~apps.seqsee.sobject.SAnchored` object.
    self.groups = set()

  def InsertElement(self, element):
    """Insert an element beyond the last element."""
    assert isinstance(element, SElement)
    anchored = SAnchored(element, [], self.num_elements,
                         self.num_elements, is_sequence_element=True)
    self.num_elements += 1
    self.elements.append(anchored)

  def InsertElements(self, *integers):
    """Utility for adding lots of integers as elements."""
    for item in integers:
      self.InsertElement(SElement(item))

  def InsertGroup(self, group):
    """Inserts a group into the workspace. It must not conflict with an existing group, else a
    ConflictingGroupException is raised."""
    conflicting_groups = tuple(self.GetConflictingGroups(group))
    if conflicting_groups:
      raise ConflictingGroupException(conflicting_groups=conflicting_groups)
    else:
      self.groups.add(group)

  def GetGroupsWithSpan(self, left_fn, right_fn):
    """Get all groups which match the constraints set by the predicate functions for each end."""
    for gp in self.groups:
      if left_fn(gp.start_pos) and right_fn(gp.end_pos):
        yield gp
    for gp in self.elements:
      if left_fn(gp.start_pos) and right_fn(gp.end_pos):
        yield gp

  def GetConflictingGroups(self, gp):
    """Get a list of groups conflicting with given group.
    
    Groups g1 and g2 conflict if one group is strictly subsumed by the other and yet is
    not an element of the other. In other words, set(g1.items) overlaps set(g2.items)
    
    .. Note:: This can be sped up if I am keeping track of supergroups.
    """
    if gp.is_sequence_element: return
    if gp in self.groups: return
    gp_items = set(gp.items)
    for other_group in self.groups:
      other_gp_items = set(other_group.items)
      if gp_items.issubset(other_gp_items) or gp_items.issuperset(other_gp_items):
        yield other_group

  def GetSuperGroups(self, anchored):
    """Returns those group that contain the given anchored as a direct element."""
    for gp in self.groups:
      if anchored in gp.items:
        yield gp
