class BatchUI:
  def __init__(self, *, controller_class):
    self.state_lock = None
    self.pause_stepping = False
    self.quitting = False
    self.stepping_thread = None

    self.controller = controller_class(ui=self, state_lock=None,
                                       controller_depth=0)
    self.RegisterQuestionHandlers()

  def AskQuestion(self, question):
    return question.Ask(self)

  def RegisterQuestionHandlers(self):
    pass
