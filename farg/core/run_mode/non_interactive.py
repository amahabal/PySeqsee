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
from farg.core.run_stats import AllStats, Mean, Median, Variance
from farg.third_party import gflags
from math import sqrt
from tkinter import ACTIVE, BOTH, Button, Canvas, END, Frame, LEFT, Listbox, N, NW, RIGHT, Scrollbar, Tk, TOP, VERTICAL, Y
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

# A few constants used by the GUI
kCanvasHeight = 520
kCanvasWidth = 500
kBaseYOffset = 20
kExptYOffset = kBaseYOffset + ((kCanvasHeight - kBaseYOffset) / 3)
kInferenceStatsYOffset = kBaseYOffset + 2 * ((kCanvasHeight - kBaseYOffset) / 3)

kPieChartXOffset = 10
kHistogramXOffset = 180
kBasicStatsXOffset = 300
kPieChartDiameter = 100
kHistogramWidth = 100
kHistogramHeight = 100

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
    #: listbox on left listing inputs.
    frame = Frame(details_frame)
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    listbox = Listbox(frame, yscrollcommand=scrollbar.set, height=25, width=70)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(side=LEFT, fill=BOTH, expand=1)
    listbox.bind('<ButtonRelease-1>', self.SelectForDisplay)
    frame.pack(side=LEFT)
    self.listbox = listbox
    #: Canvas on right for details
    self.canvas = Canvas(details_frame, width=kCanvasWidth, height=kCanvasHeight,
                         background='#FFFFFF')
    self.canvas.pack(side=LEFT)
    #: which input are we displaying the details of?
    self.display_details_for = None

    #: Thread used for running
    self.thread = None
    self.mw.bind('<KeyPress-q>', lambda e: self.Quit())
    self.mw.bind('<KeyPress-r>', lambda e: self.KickOffRun())
    self.Refresher()

  def SelectForDisplay(self, event):
    self.display_details_for = self.listbox.get(self.listbox.curselection()[0])

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
    self.listbox.delete(0, END)
    self.canvas.delete('all')
    inputs = self.stats.input_order
    if not inputs:
      return
    for idx, input in enumerate(inputs):
      self.listbox.insert(END, input)
      d1, d2 = self.stats.IsRightBetter(input)
      #print(input, d1, d2)
      color = '#FFFFFF'
      if not d1:
        if d2 == 'More Success':
          color = '#00FF00'
        elif d2 == 'Less Success':
          color = '#FF0000'
      elif d1 == 'Faster':
        if d2 == 'Less Success':
          color = '#FFFF00'
        else:
          color = '#00FF00'
      else:
        if d2 == 'More Success':
          color = '#FFFF00'
        else:
          color = '#FF0000'
      self.listbox.itemconfigure(idx, background=color)

      if input == self.display_details_for:
        self.listbox.selection_set(idx)
    if self.display_details_for:
      self.DisplayDetails()

  def DisplayDetails(self):
    """Show detailed statistics of one input."""
    self.canvas.create_text(2, 2, text=self.display_details_for, anchor=NW)
    # Display left side
    self.DisplayOneSideStats(y=kBaseYOffset, label=self.stats.left_name,
                             stats=self.stats.GetLeftStatsFor(self.display_details_for))
    self.DisplayOneSideStats(y=kExptYOffset, label=self.stats.right_name,
                             stats=self.stats.GetRightStatsFor(self.display_details_for))
    self.DisplayInferenceStats(self.stats,
                               self.display_details_for,
                               y=kInferenceStatsYOffset)

  def DisplayOneSideStats(self, *, y, label, stats):
    self.canvas.create_text(10, y, anchor=NW, text=label)
    self.CreatePieChart(kPieChartXOffset, y + 20, stats)
    self.CreateHistogram(kHistogramXOffset, y + 20, stats)
    self.DisplayBasicStats(kBasicStatsXOffset, y + 20, stats)

  def StateToColor(self, state):
    if state == b'SuccessfulCompletion':
      return '#00FF00'
    if state == b'MaxCodeletsReached':
      return '#FF0000'
    print(state)
    return '#FFFFFF'

  def CreatePieChart(self, x0, y0, stats):
    stats_per_state = stats.stats_per_state
    state_to_counts = dict((x, len(y.codelet_counts)) for x, y in stats_per_state.items())
    total_runs = sum(state_to_counts.values())
    if total_runs == 0:
      return
    start = 0
    for state, count in state_to_counts.items():
      extent = 359.9 * count / total_runs
      color = self.StateToColor(state)
      self.canvas.create_arc(x0, y0,
                             x0 + kPieChartDiameter, y0 + kPieChartDiameter,
                             start=start, extent=extent, fill=color)
      start = start + extent
    self.canvas.create_text(x0 + kPieChartDiameter / 2, y0 + kPieChartDiameter + 5,
                            anchor=N, text='%d Runs' % total_runs)

  def CreateHistogram(self, x, y, stats):
    all_runs = []
    for state, stats_for_state in stats.stats_per_state.items():
      all_runs.extend((state, x) for x in stats_for_state.codelet_counts)
    all_runs = sorted((x for x in all_runs if x[1] > 0), key=lambda x: x[1])
    count = len(all_runs)
    if count == 0:
      return
    delta_x = kHistogramWidth / count
    max_codelet_count = max(x[1] for x in all_runs)
    for idx, run in enumerate(all_runs):
      color = self.StateToColor(run[0])
      y_end = y + kHistogramHeight - kHistogramHeight * run[1] / max_codelet_count
      this_x = x + delta_x * idx
      self.canvas.create_line(this_x, y_end, this_x, y + kHistogramHeight, fill=color)
    self.canvas.create_text(x + kHistogramWidth / 2, y + kHistogramHeight + 10,
                            anchor=N, text='Max codelets: %d' % max_codelet_count)

  def DisplayBasicStats(self, x, y, stats):
    successful_completion_stats = stats.stats_per_state[b'SuccessfulCompletion']
    total_runs = sum(len(x.codelet_counts) for x in stats.stats_per_state.values())
    if total_runs == 0:
      return
    percentage = '%3.2f%%' % (100 * len(successful_completion_stats.codelet_counts) /
                              total_runs)
    self.canvas.create_text(x, y, anchor=NW, text='Success: %s' % percentage)
    codelet_counts = successful_completion_stats.codelet_counts
    if codelet_counts:
      mean_codelet_count = Mean(codelet_counts)
      median_codelet_count = Median(codelet_counts)
      self.canvas.create_text(x, y + 15, anchor=NW, text='Mean: %3.2f' % mean_codelet_count)
      self.canvas.create_text(x, y + 30, anchor=NW, text='Median: %3.2f' % median_codelet_count)

  def DisplayInferenceStats(self, stats, for_input, y):
    codelet_stats, success_stats = stats.GetComparitiveStats(for_input)
    if not codelet_stats or not success_stats:
      return
    self.canvas.create_text(10, y, anchor=NW,
                            text='means: (%3.2f, %3.2f), variance: (%3.2f, %3.2f)' %
                            (codelet_stats['left_mean'],
                             codelet_stats['right_mean'],
                             codelet_stats['left_variance'],
                             codelet_stats['right_variance']))
    self.canvas.create_text(10, y + 20, anchor=NW,
                            text='Counts: (%d, %d), k=%d, t=%3.2f, %s' %
                            (codelet_stats['n1'],
                             codelet_stats['n2'],
                             codelet_stats['df'],
                             codelet_stats['t'],
                             codelet_stats['descriptor']))

    self.canvas.create_text(10, y + 40, anchor=NW,
                            text='means: (%3.2f, %3.2f), variance: (%3.2f, %3.2f)' %
                            (success_stats['left_mean'],
                             success_stats['right_mean'],
                             success_stats['left_variance'],
                             success_stats['right_variance']))
    self.canvas.create_text(10, y + 60, anchor=NW,
                            text='Counts: (%d, %d), k=%d, t=%3.2f, %s' %
                            (success_stats['n1'],
                             success_stats['n2'],
                             success_stats['df'],
                             success_stats['t'],
                             success_stats['descriptor']))


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
