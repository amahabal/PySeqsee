# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

from farg.core.run_mode.non_interactive import RunModeNonInteractive, RunMultipleTimes, MultipleRunGUI
from farg.third_party import gflags

FLAGS = gflags.FLAGS

class BatchRunMultipleTimes(RunMultipleTimes):
  """Multiple-runner specialized for batch."""

  def GetSubprocessArguments(self, one_input_spec_arguments):
    arguments = dict(stopping_condition=FLAGS.stopping_condition,
                     stopping_condition_granularity=FLAGS.stopping_condition_granularity,
                     run_mode="single",
                     max_steps=FLAGS.max_steps,
                     eat_output=FLAGS.eat_output,
                     use_stored_ltm=FLAGS.use_stored_ltm,
                     double_mapping_resistance=FLAGS.double_mapping_resistance,
                     )
    arguments.update(one_input_spec_arguments.arguments_dict)
    return arguments

  def RunAll(self):
    print("Run started")
    for one_input_spec in self.input_spec:
      name = one_input_spec.name
      arguments = self.GetSubprocessArguments(one_input_spec)

      stats = self.gui.stats.GetRightStatsFor(name)

      for _idx in range(FLAGS.num_iterations):
        if self.gui.quitting:
          return
        result = RunModeNonInteractive.DoSingleRun(arguments)
        stats.AddData(result)


class RunModeBatch(RunModeNonInteractive):
  def __init__(self, *, controller_class, input_spec):
    print("Initialized Batch run mode")
    self.input_spec = input_spec

  def Run(self):
    gui = MultipleRunGUI(input_spec=self.input_spec,
                         multiple_runner_class=BatchRunMultipleTimes,
                         left_name='Previous',
                         right_name='Current')
    gui.mw.mainloop()
