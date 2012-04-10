from farg.run_mode.non_interactive import RunModeNonInteractive
from farg.run_stats import RunStats
from third_party import gflags


FLAGS = gflags.FLAGS

gflags.DEFINE_string('base_flags', '', 'Extra flags for base')
gflags.DEFINE_string('exp_flags', '', 'Extra flags for exp')

class RunModeSxS(RunModeNonInteractive):
  def __init__(self, *, controller_class, input_spec):
    print("Initialized SxS run mode")
    if FLAGS.base_flags == FLAGS.exp_flags:
      raise ValueError("Base and Exp flags are identical (%s). SxS makes no sense!" %
                       FLAGS.exp_flags)
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
      common_arguments = self.GetSubprocessArguments(spec)

      # Base
      stats = RunStats()
      for _idx in range(FLAGS.num_iterations):
        result = self.DoSingleRun(common_arguments, FLAGS.base_flags)
        stats.AddData(result)
      print(str(stats))

      # Exp
      stats = RunStats()
      for _idx in range(FLAGS.num_iterations):
        result = self.DoSingleRun(common_arguments, FLAGS.exp_flags)
        stats.AddData(result)
      print(str(stats))
