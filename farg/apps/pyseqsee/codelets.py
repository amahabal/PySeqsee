from farg.core.codelet import CodeletFamily


class CF_FocusOnRandomElement(CodeletFamily):
  """Randomly choose an element to focus on."""

  @classmethod
  def Run(cls, controller, *, me):
    focus = controller.workspace.SelectRandomElement()
    controller.stream.FocusOn(focusable=focus, controller=controller)


class CF_FocusOnObject(CodeletFamily):
  """Focus on the object passed in via the parameter 'focus'."""

  @classmethod
  def Run(cls, controller, focus, *, me):
    controller.stream.FocusOn(focusable=focus, controller=controller)
