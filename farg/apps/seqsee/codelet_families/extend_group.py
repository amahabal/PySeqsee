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

import logging

from farg.apps.seqsee.anchored import SAnchored
from farg.apps.seqsee.subspaces.go_beyond_known import SubspaceGoBeyondKnown
from farg.core.codelet import CodeletFamily
from farg.core.history import History
from farg.core.util import Toss, SelectWeightedByActivation
class CF_ExtendGroup(CodeletFamily):
  @classmethod
  def Run(cls, controller, item, *, me):
    if item not in controller.workspace.groups:
      History.Note("CF_ExtendGroup: item not in workspace")
      # item deleted?
      return
    # QUALITY TODO(Feb 14, 2012): Direction to extend choice can be improved.
    extend_right = True
    if (item.start_pos > 0 and Toss(0.5)):
      extend_right = False

    parts = item.items
    underlying_mapping_set = item.object.underlying_mapping_set
    if not underlying_mapping_set:
      History.Note("CF_ExtendGroup: no underlying relations")
      return
    mapping = SelectWeightedByActivation(controller.ltm, underlying_mapping_set)
    if extend_right:
      next_part = mapping.Apply(parts[-1].object)
      if not next_part:
        History.Note("CF_ExtendGroup: could not apply mapping to last part")
        return
      magnitudes = next_part.FlattenedMagnitudes()
      number_of_known_elements = len(controller.workspace.elements) - item.end_pos - 1
      if len(magnitudes) > number_of_known_elements:
        # TODO(# --- Feb 14, 2012): This is where we may go beyond known elements.
        # To the extent that the next few elements are known, ensure that they agree with
        # what's known.
        if not controller.workspace.CheckForPresence(item.end_pos + 1,
                                                     magnitudes[:number_of_known_elements]):
          return
        # The following either returns false soon if the user will not be asked, or asks
        # the user and returns the response. If the response is yes, the elements are also
        # added.
        should_continue = SubspaceGoBeyondKnown(
            controller,
            workspace_arguments=dict(basis_of_extension=item,
                                     suggested_terms=magnitudes),
            parents=[me, item]).Run()
        if not should_continue:
          return
      else:
        if not controller.workspace.CheckForPresence(item.end_pos + 1, magnitudes):
          return
      next_part_anchored = SAnchored.CreateAt(item.end_pos + 1, next_part)
      new_parts = list(parts[:])
      new_parts.append(next_part_anchored)
    else:
      flipped = mapping.FlippedVersion()
      if not flipped:
        return
      previous_part = flipped.Apply(parts[0].object)
      if not previous_part:
        return
      magnitudes = previous_part.FlattenedMagnitudes()
      if len(magnitudes) > item.start_pos:
        return
      if not controller.workspace.CheckForPresence(item.start_pos - len(magnitudes),
                                                   magnitudes):
        return
      prev_part_anchored = SAnchored.CreateAt(item.start_pos - len(magnitudes),
                                              previous_part)
      new_parts = [prev_part_anchored]
      new_parts.extend(parts)
    new_group = SAnchored.Create(new_parts,
                                 underlying_mapping_set={mapping})

    from farg.apps.seqsee.exceptions import ConflictingGroupException
    from farg.apps.seqsee.exceptions import CannotReplaceSubgroupException
    from farg.apps.seqsee.subspaces.deal_with_conflicting_groups import SubspaceDealWithConflictingGroups
    try:
      controller.workspace.Replace(item, new_group)
    except ConflictingGroupException as e:
      SubspaceDealWithConflictingGroups(
          controller,
          workspace_arguments=dict(new_group=new_group,
                                   incumbents=e.conflicting_groups),
          parents=[me, item],
          msg="Conflict when replacing item with enlarged group").Run()
    except CannotReplaceSubgroupException as e:
      SubspaceDealWithConflictingGroups(
          controller,
          workspace_arguments=dict(new_group=new_group,
                                   incumbents=e.supergroups),
          parents=[me, item],
          msg="Cannot replace subgp when extending item").Run()
