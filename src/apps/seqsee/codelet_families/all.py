from farg.codelet import Codelet, CodeletFamily
from apps.seqsee.sobject import SAnchored

class CF_FocusOn(CodeletFamily):
  """Causes the required focusable to be added to the stream."""
  @classmethod
  def Run(cls, controller, focusable):
    controller.stream.FocusOn(focusable)

class CF_GroupFromRelation(CodeletFamily):
  """Causes the required relations' ends to create a group."""
  @classmethod
  def Run(cls, controller, relation):
    anchored = SAnchored.Create(relation.first, relation.second)
    # TODO(# --- Jan 3, 2012): Can throw. Need a method to handle the exception...
    controller.ws.InsertGroup(anchored)
    controller.DisplayMessage('Groups: ' + ';'.join(str(x) for x in controller.ws.groups))
