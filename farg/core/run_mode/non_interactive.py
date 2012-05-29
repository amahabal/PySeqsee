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
from farg.core.run_stats import AllStats
from farg.third_party import gflags
from tkinter import Button, Canvas, Frame, LEFT, NW, Text, Tk, TOP
import subprocess
import sys
import threading

FLAGS = gflags.FLAGS

class RunMultipleTimes(threading.Thread):
  """Class to run the application several times on a set of inputs.

     This is the thread that does all the work (except the UI) for batch and SxS modes.
  """

  def __init__(self, *, input_spec, gui):
    """Initializes the thread and remembers the input specification for multiple runs."""
    threading.Thread.__init__(self)

    #: The input_spec is an iterable of
    #: :py:class:`farg.core.read_input_spec.SpecificationForOneRun`.
    self.input_spec = input_spec

    #: Points to the GUI controlling the run. The GUI maintains the statistics that this
    #: class's actions update.
    self.gui = gui

  def run(self):
    """The method of the thread class that is started by Start().

       Merely delegates to RunAll, which should be overriden by subclass.
    """
    self.RunAll()

class MultipleRunGUI:
  """GUI for batch and SxS modes for displaying the stats."""

  def __init__(self, *, multiple_runner_class, input_spec, left_name, right_name):
    """Initialize the GUI (sets up windows) and the instance of multiple-runner that will
       do the actual work."""
    #: The input_spec is an iterable of
    #: :py:class:`farg.core.read_input_spec.SpecificationForOneRun`.
    self.input_spec = input_spec
    #: Class responsible for the actual running multiple times.
    self.multiple_runner_class = multiple_runner_class
    #: Main window
    self.mw = mw = Tk()
    #: Statistics thus far, grouped by input.
    self.stats = AllStats(left_name=left_name, right_name=right_name)

    #: Are we in the process of quitting?
    self.quitting = False

    self.SetupButtonBar(mw)

    self.SetupArgumentsBar(mw)

    #: Has a run started? Used to ensure single run.
    self.run_started = False

    details_frame = Frame(mw)
    details_frame.pack(side=TOP)
    #: Text box on left listing inputs.
    self.text = Text(details_frame)
    self.text.pack(side=LEFT)
    #: Canvas on right for details
    self.canvas = Canvas(details_frame, width=500, height=400, background='#FFFFFF')
    self.canvas.pack(side=LEFT)
    #: which input are we displaying the details of?
    self.display_details_for = None

    #: Thread used for running
    self.thread = None
    self.mw.bind('<KeyPress-q>', lambda e: self.Quit())
    self.mw.bind('<KeyPress-r>', lambda e: self.KickOffRun())
    self.Refresher()

  def SetupButtonBar(self, mw):
    """Sets up the top button-bar."""
    button_bar = Frame(mw)
    button_bar.pack(side=TOP)
    Button(button_bar, text="Run", command=self.KickOffRun).pack(side=LEFT)

  def SetupArgumentsBar(self, mw):
    """Sets up area to choose filename and other parameters of the run."""
    arguments_bar = Frame(mw)
    arguments_bar.pack(side=TOP)

  def Quit(self):
    self.quitting = True
    if self.thread:
      self.thread.join()
    self.mw.quit()

  def Refresher(self):
    self.UpdateDisplay()
    self.mw.after(100, self.Refresher)

  def KickOffRun(self):
    if self.run_started:
      return
    self.run_started = True
    self.thread = self.multiple_runner_class(input_spec=self.input_spec, gui=self)
    self.thread.start()

  def UpdateDisplay(self):
    """Displays the Stats."""
    self.text.delete('0.0', 'end')
    self.canvas.delete('all')
    inputs = self.stats.input_order
    if not inputs:
      return
    for input in inputs:
      left_stats = self.stats.GetLeftStatsFor(input)
      if not left_stats.IsEmpty():
        self.text.insert('end', "======%s: %s======\n" % (input, self.stats.left_name))
        self.text.insert('end', str(left_stats) + "\n")
      right_stats = self.stats.GetRightStatsFor(input)
      if not right_stats.IsEmpty():
        self.text.insert('end', "======%s: %s======\n" % (input, self.stats.right_name))
        self.text.insert('end', str(right_stats) + "\n")
    self.display_details_for = inputs[0]  # Hack
    if self.display_details_for:
      self.DisplayDetails()

  def DisplayDetails(self):
    """Show detailed statistics of one input."""

    # Display left side
    self.DisplayOneSideStats(y=10, label=self.stats.left_name,
                             stats=self.stats.GetLeftStatsFor(self.display_details_for))
    self.DisplayOneSideStats(y=140, label=self.stats.right_name,
                             stats=self.stats.GetRightStatsFor(self.display_details_for))

  def DisplayOneSideStats(self, *, y, label, stats):
    self.canvas.create_text(10, y, anchor=NW, text=label)
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
