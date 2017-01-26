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

from farg.apps.seqsee.anchored import SAnchored
from farg.apps.seqsee.subspaces.deal_with_conflicting_groups import SubspaceDealWithConflictingGroups
from farg.core.codelet import CodeletFamily
from farg.apps.seqsee.exceptions import ConflictingGroupException, CannotReplaceSubgroupException
import logging

class CF_ActOnOverlappingGroups(CodeletFamily):
  @classmethod
  def Run(cls, controller, left, right, *, me):
    logging.debug("RUNNING CF_ActOnOverlappingGroups: left=%s, right=%s", str(left), str(right))
    if left not in controller.workspace.groups or right not in controller.workspace.groups:
      # Groups gone, fizzle.
      return
    if set(left.items).intersection(set(right.items)):
      # So overlap, and share elements.
      left_underlying_set = left.object.underlying_mapping_set
      right_underlying_set = right.object.underlying_mapping_set
      # TODO(# --- Jan 28, 2012): Even if the following fails, there is reason to try and
      # see how the two may be made to agree.
      if left_underlying_set and left_underlying_set.intersection(right_underlying_set):
        # This calls out for merging!
        new_group_items = sorted(set(left.items).union(set(right.items)),
                                 key=lambda x: x.start_pos)
        logging.debug("New group items: %s",
                      '; '.join(str(x) for x in new_group_items))
        new_group = SAnchored.Create(
            new_group_items,
            underlying_mapping_set=left_underlying_set.intersection(right_underlying_set))
        try:
          controller.workspace.Replace((left, right), new_group)
        except ConflictingGroupException as e:
          SubspaceDealWithConflictingGroups(
              controller,
              workspace_arguments=dict(new_group=new_group,
                                       incumbents=e.conflicting_groups)).Run()
        except CannotReplaceSubgroupException as e:
          SubspaceDealWithConflictingGroups(
              controller,
              workspace_arguments=dict(new_group=new_group,
                                       incumbents=e.supergroups)).Run()
