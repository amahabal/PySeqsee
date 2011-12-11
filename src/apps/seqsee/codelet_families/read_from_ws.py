from farg.codelet import Codelet, CodeletFamily

class CF_ReadFromWS(CodeletFamily):
  @classmethod
  def Run(cls, controller):
    choice = controller.ws.ChooseItemToFocusOn()
    controller.stream.FocusOn(choice)
