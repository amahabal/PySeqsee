from tide.run_mode.run_mode import RunMode

class RunModeGUI(RunMode):
  def __init__(self, *, controller_class, ui_class, stopping_condition_fn=None):
    print("Initialized a GUI run mode")
    self.ui = ui_class(controller_class=controller_class,
                       stopping_condition_fn=stopping_condition_fn)

  def Run(self):
    self.Refresher()
    self.ui.mw.mainloop()

  def Refresher(self):
    self.ui.UpdateDisplay()
    self.ui.mw.after(100, self.Refresher)
