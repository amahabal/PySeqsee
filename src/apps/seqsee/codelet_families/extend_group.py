from farg.codelet import CodeletFamily
from farg.util import Toss
from apps.seqsee.anchored import SAnchored
from apps.seqsee.subspaces.go_beyond_known import SubspaceGoBeyondKnown

class CF_ExtendGroup(CodeletFamily):
  @classmethod
  def Run(cls, controller, item):
    if item not in controller.workspace.groups:
      # item deleted?
      return
    # QUALITY TODO(Feb 14, 2012): Direction to extend choice can be improved.
    extend_right = True
    if (item.start_pos > 0 and Toss(0.5)):
      extend_right = False

    parts = item.items
    underlying_mapping = item.object.underlying_mapping
    if extend_right:
      next_part = underlying_mapping.Apply(parts[-1].object)
      if not next_part:
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
                                     suggested_terms=magnitudes))
        if not should_continue:
          return
      else:
        if not controller.workspace.CheckForPresence(item.end_pos + 1, magnitudes):
          return
      next_part_anchored = SAnchored.CreateAt(item.end_pos + 1, next_part)
      new_parts = list(parts[:])
      new_parts.append(next_part_anchored)
    else:
      flipped = underlying_mapping.FlippedVersion()
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
      print(new_parts)
    new_group = SAnchored.Create(*new_parts,
                                 underlying_mapping=underlying_mapping)

    from farg.exceptions import ConflictingGroupException
    from farg.exceptions import CannotReplaceSubgroupException
    from apps.seqsee.subspaces.deal_with_conflicting_groups import SubspaceDealWithConflictingGroups
    try:
      controller.workspace.Replace(item, new_group)
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
