from farg.codelet import CodeletFamily
from apps.seqsee.anchored import SAnchored
from farg.exceptions import ConflictingGroupException
from apps.seqsee.subspaces.deal_with_conflicting_groups import SubspaceDealWithConflictingGroups

class CF_FocusOn(CodeletFamily):
  """Causes the required focusable to be added to the stream."""
  @classmethod
  def Run(cls, controller, focusable):
    controller.stream.FocusOn(focusable)

class CF_GroupFromRelation(CodeletFamily):
  """Causes the required relations' ends to create a group."""
  @classmethod
  def Run(cls, controller, relation):
    # If there is a group spanning the proposed group, perish the thought.
    left, right = relation.first.start_pos, relation.second.end_pos
    from apps.seqsee.util import GreaterThanEq, LessThanEq
    if tuple(controller.ws.GetGroupsWithSpan(LessThanEq(left), GreaterThanEq(right))):
      return
    anchored = SAnchored.Create(relation.first, relation.second,
                                underlying_mapping=relation.mapping)
    try:
      controller.ws.InsertGroup(anchored)
    except ConflictingGroupException as e:
      SubspaceDealWithConflictingGroups(
          controller,
          workspace_arguments=dict(new_group=anchored,
                                   incumbents=e.conflicting_groups))

class CF_DescribeAs(CodeletFamily):
  """Attempt to describe item as belonging to category."""
  @classmethod
  def Run(cls, controller, item, category):
    if not item.IsKnownAsInstanceOf(category):
      item.DescribeAs(category)

class CF_RemoveSpuriousRelations(CodeletFamily):
  """Removes relations between all pairs (A, B) where both belong to supuergroups but their
     supergroups don't overlap.
  """
  @classmethod
  def Run(cls, controller):
    ws = controller.workspace
    supergroups_map = ws.CalculateSupergroupMap()
    for element in ws.elements:
      supergps = supergroups_map[element]
      if not supergps:
        continue
      relations_to_remove = []
      for relation in element.relations:
        if relation.first == element:
          other_end = relation.second
        else:
          other_end = relation.first
        other_supergps = supergroups_map[other_end]
        if not other_supergps:
          continue
        if supergps.intersection(other_supergps):
          continue
        other_end.relations.discard(relation)
        relations_to_remove.append(relation)
      for relation in relations_to_remove:
        element.relations.discard(relation)
