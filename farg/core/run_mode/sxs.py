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

from farg.core.run_mode.non_interactive import (RunModeNonInteractive, RunMultipleTimes,
                                                MultipleRunGUI)
import sys
import farg_flags

class SxSRunMultipleTimes(RunMultipleTimes):
  """Multiple-runner specialized for SxS."""

  def GetSubprocessArguments(self, one_input_spec_arguments):
    arguments = []
    arguments.append('--stopping_condition=%s' % farg_flags.FargFlags.stopping_condition)
    arguments.append('--stopping_condition_granularity=%s' % farg_flags.FargFlags.stopping_condition_granularity)
    arguments.append('--run_mode=single')
    arguments.append('--max_steps=%s' % farg_flags.FargFlags.max_steps)
    arguments.append('--eat_output')
    if farg_flags.FargFlags.use_stored_ltm:
      arguments.append('--use_stored_ltm')
    else:
      arguments.append('--nouse_stored_ltm')
    arguments.append('--double_mapping_resistance=%s' % farg_flags.FargFlags.double_mapping_resistance)
    arguments.extend(one_input_spec_arguments.arguments_list)
    return arguments

  def RunAll(self):
    for one_input_spec in self.input_spec:
      name = one_input_spec.name
      common_arguments = self.GetSubprocessArguments(one_input_spec)

      for _idx in range(farg_flags.FargFlags.num_iterations):
        left_stats = self.gui.stats.GetLeftStatsFor(name)
        if self.gui.quitting:
          return
        result = RunModeNonInteractive.DoSingleRun(common_arguments, farg_flags.FargFlags.base_flags)
        left_stats.AddData(result)

        right_stats = self.gui.stats.GetRightStatsFor(name)
        if self.gui.quitting:
          return
        result = RunModeNonInteractive.DoSingleRun(common_arguments, farg_flags.FargFlags.exp_flags)
        right_stats.AddData(result)


class RunModeSxS(RunModeNonInteractive):
  def __init__(self, *, controller_class, input_spec):
    print('Initialized SxS run mode')
    if farg_flags.FargFlags.base_flags == farg_flags.FargFlags.exp_flags:
      print('Base and Exp flags are identical (%s). SxS makes no sense!' %
            farg_flags.FargFlags.exp_flags)
      sys.exit(1)
    self.input_spec = input_spec

  def Run(self):
    gui = MultipleRunGUI(input_spec=self.input_spec,
                         multiple_runner_class=SxSRunMultipleTimes,
                         left_name='Base',
                         right_name='Experiment')
    gui.mw.mainloop()
