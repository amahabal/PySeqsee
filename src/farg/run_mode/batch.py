from farg.run_mode.non_interactive import RunModeNonInteractive
from farg.run_stats import RunStats
from third_party import gflags

FLAGS = gflags.FLAGS

class RunModeBatch(RunModeNonInteractive):
  def __init__(self, *, controller_class, input_spec):
    print("Initialized Batch run mode")
    self.input_spec = input_spec

  def GetSubprocessArguments(self, one_input_spec_arguments):
    arguments = dict(stopping_condition=FLAGS.stopping_condition,
                     stopping_condition_granularity=FLAGS.stopping_condition_granularity,
                     run_mode="single",
                     max_steps=FLAGS.max_steps,
                     )
    arguments.update(one_input_spec_arguments)
    return arguments

  def Run(self):
    for one_input_spec in self.input_spec:
      name = one_input_spec['name']
      spec = one_input_spec['spec']
      print("======%s======" % name)
      arguments = self.GetSubprocessArguments(spec)

      stats = RunStats()

      for _idx in range(FLAGS.num_iterations):
        result = self.DoSingleRun(arguments)
        stats.AddData(result)

      print(str(stats))
