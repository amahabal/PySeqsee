class BatchUI:
  def __init__(self, *, controller_class, stopping_condition_fn):
    self.state_lock = None
    self.pause_stepping = False
    self.quitting = False
    self.stepping_thread = None

    self.controller = controller_class(ui=self, state_lock=None,
                                       controller_depth=0,
                                       stopping_condition=stopping_condition_fn)
    self.RegisterQuestionHandlers()

  def AskQuestion(self, question):
    return question.Ask(self)

  def RegisterQuestionHandlers(self):
    pass

  def Run(self):
    self.controller.RunUptoNSteps(1000)
