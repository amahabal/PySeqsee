from farg.codelet import Codelet, CodeletFamily
from apps.seqsee.anchored import SAnchored

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
    # TODO(# --- Jan 3, 2012): Can throw. Need a method to handle the exception...
    controller.ws.InsertGroup(anchored)
    #controller.DisplayMessage('Groups: ' +
    #                          ';'.join(str(x) for x in controller.ws.groups))
