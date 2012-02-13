"""The workspace is the virtual blackboard on which various codelets make annotations about
   relationships that have been seen between entities and groups that have been formed.

   The workspace contains three main types of objects: elements such as a "7", groups such
   as "(2 3)" and relations between these entities.  The relationships are not directly
   entered into the workspace.  They are kept with the groups and elements between which the
   relationship holds.

   The workspace makes a consistency guarantee that no groups conflict with each other at any
   time.  It is important to note that overlap does not necessarily imply a conflict.  If the
   overlap between two groups forms a complete unit within each group, no conflict exists.

   For a group in the workspace, it is a required that its parts be a part of the workspace
   as well.  Also, it is not permissible for two distinct groups to be at the same location.
   What this means is that for overlapping groups the overlap itself represents a group or
   an element in the workspace.

   The method InsertGroup is used to add new groups.  If adding this group leads to an
   inconsistent state, it is not added and a ConflictingGroupException is raised.  Note that
   the consistency guarantee implies that adding the group may involve adding all its
   subgroups, and one of these may conflict with an existing group.

   .. warning:

      This is likely to be quite inefficient. Keep an eye open for how slow this actually is.
"""

from apps.seqsee.anchored import SAnchored
from apps.seqsee.sobject import SElement
from apps.seqsee.util import Exactly
from farg.exceptions import FargError, ConflictingGroupException, CannotReplaceSubgroupException
from farg.util import WeightedChoice
import logging

logger = logging.getLogger(__name__)

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
    """Inserts a group into the workspace. It must not conflict with an existing group, else
       a ConflictingGroupException is raised.

       Returns a new group formed from things added to the workspace.
    """
    conflicting_groups = tuple(self.GetConflictingGroups(group))
    if conflicting_groups:
      logger.warning('Conflicts while adding %s: %s', group,
                      '; '.join(str(x) for x in conflicting_groups))
      raise ConflictingGroupException(conflicting_groups=conflicting_groups)
    else:
      return self._PlonkIntoPlace(group)

  def _PlonkIntoPlace(self, group):
    """Anchors the group into the workspace. Assumes that conflicts have already been checked
       for.
    """
    groups_at_this_location = list(self.GetGroupsWithSpan(Exactly(group.start_pos),
                                                          Exactly(group.end_pos)))
    if groups_at_this_location:
      group_at_this_location = groups_at_this_location[0] # There can be only 1
      if (group.object.underlying_mapping and
          not group_at_this_location.object.underlying_mapping):
        group_at_this_location.object.underlying_mapping = group.object.underlying_mapping
      return group_at_this_location

    # Construct one
    pieces = [self._PlonkIntoPlace(x) for x in group.items]
    new_object = SAnchored.Create(*pieces,
                                  underlying_mapping=group.object.underlying_mapping)
    # TODO(# --- Jan 30, 2012): Copy categories as well.
    self.groups.add(new_object)
    return new_object

  def GetGroupsWithSpan(self, left_fn, right_fn):
    """Get all groups which match the constraints set by the predicate functions for each
       end.
    """
    # TODO(#33 --- Dec 28, 2011): Rename to GetObjectsWithSpan.
    for gp in self.groups:
      if left_fn(gp.start_pos) and right_fn(gp.end_pos):
        yield gp
    for gp in self.elements:
      if left_fn(gp.start_pos) and right_fn(gp.end_pos):
        yield gp

  def GetConflictingGroups(self, gp):
    """Get a list of groups conflicting with given group.

       Only maximal groups are returned, where the relative order is based on being a
       subgroup (i.e., if A is a part of B, and both conflict, B is returned; note that if A
       conflicts with the group under consideration, so does B).
       .. Note:: This can be sped up if I am keeping track of supergroups.
    """
    if gp.is_sequence_element: return
    if gp in self.groups: return

    groups_at_this_location = list(self.GetGroupsWithSpan(Exactly(gp.start_pos),
                                                          Exactly(gp.end_pos)))
    if groups_at_this_location:
      # If something lies at exactly this location, it had better have the same structure.
      group_at_this_location = groups_at_this_location[0]  # Can only be one.
      if group_at_this_location.Structure() == gp.Structure():
        return
      else:
        yield self.SomeMaximalSuperGroup(group_at_this_location)
        return

    # See if any subgroup conflicts.
    gp_items = set(gp.items)
    for subgroup in gp_items:
      conflicts = list(self.GetConflictingGroups(subgroup))
      if conflicts:
        for conflict in conflicts:
          yield conflict
        return

    # Since we got here, any subgroup is fine individually. The only thing that may go wrong
    # is that there is overlap of more than one subgroup with an existing group (i.e., there
    # exists a (1, 2, 3, 4) and we are adding (3, 4, 5, 6)).

    existsing_group_items = set()
    for item in gp_items:
      # If a group exists with these ends, keep it in existing groups.
      objects_with_same_span = list(self.GetGroupsWithSpan(Exactly(item.start_pos),
                                                           Exactly(item.end_pos)))
      if objects_with_same_span:
        existsing_group_items.add(objects_with_same_span[0])

    for other_group in self.groups:
      other_gp_items = set(other_group.items)
      overlap = existsing_group_items.intersection(other_gp_items)
      if len(overlap) >= 2:
        yield self.SomeMaximalSuperGroup(other_group)

  def GetSuperGroups(self, anchored):
    """Returns those group that contain the given anchored as a direct element."""
    for gp in self.groups:
      if anchored in gp.items:
        yield gp

  def SomeMaximalSuperGroup(self, gp):
    """Returns some super* group, if any, or returns self."""
    for supergp in self.GetSuperGroups(gp):
      return self.SomeMaximalSuperGroup(supergp)
    # We reach here if no supergroup exists.
    return gp

  def Replace(self, original_gps, new_group):
    """Replace original group with new group unless the new group is going to cause conflicts.
    
       If the new group will cause conflicts, a ConflictingGroupException is raised.
    """
    if not isinstance(original_gps, tuple):
      original_gps = (original_gps,)
    # Original group had better be present:
    for original_gp in original_gps:
      if not original_gp in self.groups:
        raise FargError("Group being replaced not in WS!")
      supergroups = list(self.GetSuperGroups(original_gp))
      if supergroups:
        raise CannotReplaceSubgroupException(supergroups)
    # The idea here is to temporarily delete original group from groups in the ws, see if
    # new_group fits in. If it does, we may need to do more work such as fixing relations.
    # TODO(# --- Jan 27, 2012): Complete this.
    for original_gp in original_gps:
      self.groups.discard(original_gp)
    try:
      self.InsertGroup(new_group)
    except ConflictingGroupException as e:
      for original_gp in original_gps:
        self.groups.add(original_gp)
      raise e

  def ChooseItemToFocusOn(self):
    """Choose an item from the WS to focus on.
    
    Will currently be elements or groups."""
    def ThingsToChooseFrom(ws):
      """Yields two-tuples of things to choose from, the second being weight."""
      # TODO(#34 --- Dec 28, 2011): Need notion of strength. Will bias these weights.
      for element in ws.elements:
        yield (element, 0.5)
      for gp in ws.groups:
        yield (gp, 1.0)

    return WeightedChoice(ThingsToChooseFrom(self))

  def GetItemAt(self, start_pos, end_pos):
    """Returns the sole object with this span. Throws FargError if not found."""
    for group in self.groups:
      if group.start_pos == start_pos and group.end_pos == end_pos:
        return group
    if start_pos == end_pos:
      for element in self.elements:
        if element.start_pos == start_pos:
          return element
    raise FargError("GetItemAt has no item to return.")
