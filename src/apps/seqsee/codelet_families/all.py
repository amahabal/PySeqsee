from farg.codelet import Codelet, CodeletFamily

class CF_FocusOn(CodeletFamily):
  """Causes the required focusable to be added to the stream."""
  @classmethod
  def Run(cls, controller, focusable):
    controller.stream.FocusOn(focusable)
