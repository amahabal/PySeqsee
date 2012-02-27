from farg.codelet import CodeletFamily
from apps.seqsee.anchored import SAnchored
from farg.exceptions import ConflictingGroupException, CannotReplaceSubgroupException

import logging
from apps.seqsee.subspaces.deal_with_conflicting_groups import SubspaceDealWithConflictingGroups

logger = logging.getLogger(__name__)

class CF_ActOnOverlappingGroups(CodeletFamily):
  @classmethod
  def Run(cls, controller, left, right):
    if left not in controller.ws.groups or right not in controller.ws.groups:
      # Groups gone, fizzle.
      return
    if set(left.items).intersection(set(right.items)):
      # So overlap, and share elements.
      left_underlying = left.object.underlying_mapping
      right_underlying = right.object.underlying_mapping
      # TODO(# --- Jan 28, 2012): Even if the following fails, there is reason to try and
      # see how the two may be made to agree.
      if left_underlying and left_underlying == right_underlying:
        # This calls out for merging!
        new_group_items = sorted(set(left.items).union(set(right.items)),
                                 key=lambda x: x.start_pos)
        logger.debug("New group items: %s",
                     '; '.join(str(x) for x in new_group_items))
        new_group = SAnchored.Create(*new_group_items, underlying_mapping=left_underlying)
        try:
          controller.ws.Replace((left, right), new_group)
        except ConflictingGroupException as e:
          SubspaceDealWithConflictingGroups(
              controller,
              workspace_arguments=dict(new_group=new_group,
                                       incumbents=e.conflicting_groups))
        except CannotReplaceSubgroupException as e:
          SubspaceDealWithConflictingGroups(
              controller,
              workspace_arguments=dict(new_group=new_group,
                                       incumbents=e.supergroups))
