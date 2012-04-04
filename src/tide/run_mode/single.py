from tide.run_mode.non_interactive import RunModeNonInteractive
from third_party import gflags
from farg.exceptions import StoppingConditionMet

FLAGS = gflags.FLAGS

class RunModeSingle(RunModeNonInteractive):
  def __init__(self, *, controller_class, ui_class, stopping_condition_fn):
    self.ui = ui_class(controller_class=controller_class,
                       stopping_condition_fn=stopping_condition_fn)

  def Run(self):
    try:
      self.ui.Run()
    except StoppingConditionMet as e:
      print('StoppingConditionMet %d' % e.codelet_count)
