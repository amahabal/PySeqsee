from tide.run_mode.non_interactive import RunModeNonInteractive
class RunModeBatch(RunModeNonInteractive):
  def __init__(self, *, controller_class, ui_class, stopping_condition_fn=None):
    print("Initialized Batch run mode")
    self.ui = ui_class(controller_class=controller_class,
                       stopping_condition_fn=stopping_condition_fn)

  def Run(self):
    self.ui.Run()
