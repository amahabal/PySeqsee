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

from collections import defaultdict
import farg_flags
from farg.core.run_mode.non_interactive import RunModeNonInteractive, RunMultipleTimes, MultipleRunGUI
from farg.core.run_stats import RunStats
import os.path

class BatchRunMultipleTimes(RunMultipleTimes):
  """Multiple-runner specialized for batch."""

  def GetSubprocessArguments(self, one_input_spec_arguments):
    arguments = []
    arguments.append('--stopping_condition=%s' % farg_flags.FargFlags.stopping_condition)
    arguments.append('--stopping_condition_granularity=%s' % farg_flags.FargFlags.stopping_condition_granularity)
    arguments.append('--run_mode=single')
    arguments.append('--max_steps=%s' % farg_flags.FargFlags.max_steps)
    if farg_flags.FargFlags.use_stored_ltm:
      arguments.append('--use_stored_ltm')
    else:
      arguments.append('--nouse_stored_ltm')
    arguments.append('--double_mapping_resistance=%s' % farg_flags.FargFlags.double_mapping_resistance)
    arguments.extend(one_input_spec_arguments.arguments_list)
    return arguments

  def RunAll(self):
    self.gui.stats.left_stats = self.LoadPreviousStats()
    for one_input_spec in self.input_spec:
      name = one_input_spec.name
      arguments = self.GetSubprocessArguments(one_input_spec)
      print("arguments=", arguments)

      stats = self.gui.stats.GetRightStatsFor(name)

      for _idx in range(farg_flags.FargFlags.num_iterations):
        if self.gui.quitting:
          return
        result = RunModeNonInteractive.DoSingleRun(arguments)
        stats.AddData(result)
    self.SaveCurrent()

  def LoadPreviousStats(self):
    """Load stats from previous run, if any."""
    filename = self.GetPreviousSavedFilename()
    if filename and os.path.exists(filename):
      import pickle
      infile = open(filename, "rb")
      return pickle.load(infile)
    return defaultdict(RunStats)

  def SaveCurrent(self):
    """Save current stats for future comparison."""
    filename = self.GetSaveFilename()
    outfile = open(filename, "wb")
    import pickle
    pickle.dump(self.gui.stats.right_stats, outfile)

  def GetPreviousSavedFilename(self):
    """Returns the filename from which to read stats of previous run, if any."""
    from os import listdir
    files = listdir(farg_flags.FargFlags.stats_directory)
    if files:
      return os.path.join(farg_flags.FargFlags.stats_directory, max(files))
    return ''

  def GetSaveFilename(self):
    """Filename to store current stats in."""
    import time
    timestamp = time.strftime('%Y-%m-%d-%H-%M-%S')
    return os.path.join(farg_flags.FargFlags.stats_directory, timestamp)

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
