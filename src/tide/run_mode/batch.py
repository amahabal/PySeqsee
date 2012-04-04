from tide.run_mode.non_interactive import RunModeNonInteractive
from third_party import gflags

FLAGS = gflags.FLAGS

class RunModeBatch(RunModeNonInteractive):
  def __init__(self, *, controller_class, ui_class, stopping_condition_fn=None,
               input_spec):
    print("Initialized Batch run mode")
    self.input_spec = input_spec
    self.ui = ui_class(controller_class=controller_class,
                       stopping_condition_fn=stopping_condition_fn)

  def GetSubprocessArguments(self, one_input_spec_arguments):
    arguments = dict(stopping_condition=FLAGS.stopping_condition,
                     stopping_condition_granularity=FLAGS.stopping_condition_granularity,
                     run_mode="single_run",
                     )
    arguments.update(one_input_spec_arguments)
    return arguments

  def Run(self):
    for one_input_spec in self.input_spec:
      name = one_input_spec['name']
      spec = one_input_spec['spec']
      print("======%s======" % name)
      arguments = self.GetSubprocessArguments(spec)
      self.DoSingleRun(arguments)
    self.ui.Run()
