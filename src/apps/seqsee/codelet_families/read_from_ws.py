from farg.codelet import CodeletFamily
from apps.seqsee.subspaces.choose_item_to_focus_on import SubspaceSelectObjectToFocusOn

class CF_ReadFromWS(CodeletFamily):
  @classmethod
  def Run(cls, controller):
    choice = SubspaceSelectObjectToFocusOn(controller,
                                           parent_ws=controller.ws)
    controller.stream.FocusOn(choice)
