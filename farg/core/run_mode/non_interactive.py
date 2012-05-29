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

from farg.core.run_mode.run_mode import RunMode
from farg.core.run_stats import RunStats, AllStats
from farg.third_party import gflags
from tkinter import Button, Frame, LEFT, Text, Tk, TOP
import subprocess
import sys
import threading

FLAGS = gflags.FLAGS

class RunMultipleTimes(threading.Thread):
  """Runs controller for upto n steps.
  
  Checking each time if we have not been asked to pause."""

  def __init__(self, input_spec, gui):
    threading.Thread.__init__(self)
    self.input_spec = input_spec
    self.gui = gui

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

  def run(self):
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


class BatchModeGUI:
  """GUI for displaying results of the batch mode or SxS mode."""

  def __init__(self, input_spec):
    """Set up the UI windows."""
    #: Input specification for what inputs to run on.
    self.input_spec = input_spec
    #: Main window
    self.mw = mw = Tk()
    #: Statistics thus far, grouped by input.
    self.stats = AllStats(left_name='Previous', right_name='Current')

    #: Are we in the process of quitting?
    self.quitting = False

    self.SetupButtonBar(mw)

    self.SetupArgumentsBar(mw)

    #: Has a run started? Used to ensure single run.
    self.run_started = False

    self.text = Text(mw)
    self.text.pack(side=TOP)

    #: Thread used for running
    self.thread = None
    self.mw.bind('<KeyPress-q>', lambda e: self.Quit())
    self.mw.bind('<KeyPress-r>', lambda e: self.KickOffRun())
    self.Refresher()

  def Quit(self):
    self.quitting = True
    self.thread.join()
    self.mw.quit()

  def Refresher(self):
    self.UpdateDisplay()
    self.mw.after(100, self.Refresher)


  def SetupButtonBar(self, mw):
    """Sets up the top button-bar."""
    button_bar = Frame(mw)
    button_bar.pack(side=TOP)
    Button(button_bar, text="Run", command=self.KickOffRun).pack(side=LEFT)

  def SetupArgumentsBar(self, mw):
    """Sets up area to choose filename and other parameters of the run."""
    arguments_bar = Frame(mw)
    arguments_bar.pack(side=TOP)


  def KickOffRun(self):
    if self.run_started:
      return
    self.run_started = True
    self.thread = RunMultipleTimes(self.input_spec, self)
    self.thread.start()

  def UpdateDisplay(self):
    """Displays the Stats."""
    self.text.delete('0.0', 'end')
    inputs = self.stats.input_order
    for input in inputs:
      right_stats = self.stats.GetRightStatsFor(input)
      self.text.insert('end', "======%s======\n" % input)
      self.text.insert('end', str(right_stats) + "\n")



class RunModeNonInteractive(RunMode):
  @classmethod
  def DoSingleRun(cls, cmdline_arguments_dict, extra_arguments=None):
    arguments = []  # Collect arguments to pass to subprocess
    arguments.append(sys.executable)  # Python executable
    arguments.append(sys.argv[0])  # The script used to run this mode (e.g., run_seqsee.py)

    arguments.extend('--%s=%s' % (str(k), str(v)) for k, v in cmdline_arguments_dict.items())
    if extra_arguments:
      arguments.append(extra_arguments)
    # print(arguments)
    return subprocess.check_output(arguments)
