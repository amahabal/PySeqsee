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
"""Sets up GUI displaying statistics for batch or SxS modes.

Sets up a window where all inputs and their progress may be tracked.

The inputs are shown in the left panel, and possibly color-coded according to
whether the current run is progressing better than the prior run. For SxS,
"prior run" is the base side, whereas in the batch mode it is the last time the
batch mode was run.
"""
from abc import ABCMeta, abstractmethod  # Metaclass confuses pylint: disable=W0611
from subprocess import CalledProcessError
import subprocess
import sys
import threading
from tkinter import Canvas, Frame, Label, Listbox, Scrollbar, Tk
from tkinter.constants import BOTH, END, LEFT, N, NW, RIGHT, SINGLE, TOP, VERTICAL, X, Y

from farg.core.run_mode.run_mode import RunMode
from farg.core.run_stats import AllStats, Mean, Median
import farg.flags as farg_flags


class RunMultipleTimes(threading.Thread, metaclass=ABCMeta):
  """Class to run the application several times on a set of inputs.

     This is the thread that does all the work (except the UI) for batch and SxS
     modes.

     It keeps a pointer to the GUI and updates the stats (owned by the UI).
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

  def GetSubprocessArguments(self, one_input_spec_arguments):
    arguments = []
    arguments.append('--run_mode=single')
    arguments.append('--max_steps=%s' % farg_flags.FargFlags.max_steps)
    if farg_flags.FargFlags.use_stored_ltm:
      arguments.append('--use_stored_ltm')
    else:
      arguments.append('--nouse_stored_ltm')
    arguments.extend(one_input_spec_arguments.arguments_list)
    return arguments

  @abstractmethod
  def RunAll(self):
    """Run all the inputs as many times as appropriate.

    Should be over-ridden by subclasses. SxS and Batch would differ slightly
    here.
    """
    pass

  def run(self):  # This name is stipulated by the superclass. pylint:disable=C0103
    """The method of the thread class that is started by Start().

       Merely delegates to RunAll, which should be overriden by subclass.
    """
    self.gui.status_label_text = 'Running'
    self.RunAll()
    self.gui.status_label_text = 'Complete'


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

kDisplayColorDict = dict(((('', ''), '#FFFFFF'), (
    ('', 'More Success'), '#00FF00'), (('', 'Less Success'), '#FF0000'), (
        ('Faster', ''), '#00FF00'), (('Faster', 'More Success'), '#00FF00'), (
            ('Faster', 'Less Success'), '#FFFF00'), (('Slower', ''), '#FF0000'),
                          (('Slower', 'More Success'),
                           '#FFFF00'), (('Slower', 'Less Success'), '#FF0000')))

kStateToColor = dict(((b'SuccessfulCompletion', '#00FF00'),
                      (b'MaxCodeletsReached', '#FF0000')))


def StateToColor(state):
  """Convert state string to color for PieChart."""
  if state in kStateToColor:
    return kStateToColor[state]
  print('Found no color for %s' % state)
  return '#FFFFFF'


class MultipleRunGUI:
  """GUI for batch and SxS modes for displaying the stats."""

  def __init__(self, *, multiple_runner_class, input_spec, left_name,
               right_name):
    """Sets up windows and the instance of RunMultipleTimes that will do the actual work."""
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

    self.status_label = Label(
        mw, text='Not Started', font=('Times', 20), foreground='#000000')
    self.status_label_text = self.status_label.cget('text')
    self.status_label.pack(side=TOP, expand=True, fill=X)

    #: Has a run started? Used to ensure single run.
    self.run_started = False

    details_frame = Frame(mw)
    details_frame.pack(side=TOP)
    #: listbox on left listing inputs.
    frame = Frame(details_frame)
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    listbox = Listbox(
        frame,
        yscrollcommand=scrollbar.set,
        height=25,
        width=70,
        selectmode=SINGLE)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(side=LEFT, fill=BOTH, expand=1)
    listbox.bind('<ButtonRelease-1>', self.SelectForDisplay, '+')
    frame.pack(side=LEFT)
    self.listbox = listbox
    #: Canvas on right for details
    self.canvas = Canvas(
        details_frame,
        width=kCanvasWidth,
        height=kCanvasHeight,
        background='#FFFFFF')
    self.canvas.pack(side=LEFT)
    #: which input are we displaying the details of?
    self.display_details_for = None

    #: Thread used for running
    self.thread = None
    self.mw.bind('<KeyPress-q>', lambda e: self.Quit())
    self.mw.bind('<KeyPress-r>', lambda e: self.KickOffRun())
    self.Refresher()
    self.mw.after(1000, self.KickOffRun)

  def SelectForDisplay(self, _event):
    """Event-handler called when an input was selected for detailed display."""
    selected = self.listbox.curselection()
    if not selected:
      selected = ['0']
    self.display_details_for = self.listbox.get(selected[0])

  def Quit(self):
    """Called when the user has indicated that the application should Quit.

    Waits for any ongoing run to finish, and then destroys windows.
    """
    self.quitting = True
    if self.thread:
      self.thread.join()
    self.mw.quit()

  def Refresher(self):
    """Repeatedly refreshes the display."""
    self.UpdateDisplay()
    self.mw.after(100, self.Refresher)

  def KickOffRun(self):
    """Start run if it has not already started."""
    if self.run_started:
      return
    self.run_started = True
    self.thread = self.multiple_runner_class(
        input_spec=self.input_spec, gui=self)
    self.thread.start()

  def UpdateDisplay(self):
    """Displays the Stats."""
    current_selection = self.listbox.curselection()
    self.listbox.delete(0, END)
    self.canvas.delete('all')
    inputs = self.stats.input_order
    self.status_label.configure(text=self.status_label_text)
    if not inputs:
      return
    for idx, input_string in enumerate(inputs):
      if input_string == self.display_details_for:
        self.listbox.insert(END, '%s   <---' % input_string)
      else:
        self.listbox.insert(END, input_string)
      codelet_count_comparison, success_comparison = self.stats.IsRightBetter(
          input_string)
      color = kDisplayColorDict[(codelet_count_comparison, success_comparison)]
      self.listbox.itemconfigure(idx, background=color)

    if self.display_details_for:
      self.DisplayDetails()
    if current_selection:
      self.listbox.selection_set(current_selection[0])

  def DisplayDetails(self):
    """Show detailed statistics of one input.

    Details are shown for whatever input is present in self.display_details_for.
    """
    self.canvas.create_text(2, 2, text=self.display_details_for, anchor=NW)
    # Display left side
    self.DisplayOneSideStats(
        y=kBaseYOffset,  # Confused by * is pylint: disable=E1123,C6010
        label=self.stats.left_name,
        stats=self.stats.GetLeftStatsFor(self.display_details_for))
    self.DisplayOneSideStats(
        y=kExptYOffset,  # Confused by * is pylint: disable=E1123,C6010
        label=self.stats.right_name,
        stats=self.stats.GetRightStatsFor(self.display_details_for))
    self.DisplayInferenceStats(
        self.stats, self.display_details_for, y=kInferenceStatsYOffset)

  def DisplayOneSideStats(self, *, y, label, stats):
    """Display stats for one of the to sides for one input.

      y: Y-offset where to display.
      label: Name of the side. Will probably be one of "previous", "current",
      "base", or
      "expt".
      stats: Statistics for this run. This is a
      :py:class:`farg.core.run_stats.RunStats`
      object.
    """
    self.canvas.create_text(10, y, anchor=NW, text=label)
    self.CreatePieChart(kPieChartXOffset, y + 20, stats)
    self.CreateHistogram(kHistogramXOffset, y + 20, stats)
    self.DisplayBasicStats(kBasicStatsXOffset, y + 20, stats)

  def CreatePieChart(self, x_offset, y_offset, stats):
    """Create PieChart.

    Args:
      x_offset: X-offset for Pie.
      y_offset: Y-offset for Pie.
      stats: Stats to display. Instance of
        :py:class:`~farg.core.run_stats.RunStats`.
    """
    stats_per_state = stats.stats_per_state
    state_to_counts = dict((x, len(y.codelet_counts))
                           for x, y in stats_per_state.items())
    total_runs = sum(state_to_counts.values())
    if total_runs == 0:
      return
    start = 0
    for state, count in state_to_counts.items():
      extent = 359.9 * count / total_runs
      color = StateToColor(state)
      self.canvas.create_arc(
          x_offset,
          y_offset,
          x_offset + kPieChartDiameter,
          y_offset + kPieChartDiameter,
          start=start,
          extent=extent,
          fill=color)
      start += extent
    self.canvas.create_text(
        x_offset + kPieChartDiameter / 2,
        y_offset + kPieChartDiameter + 5,
        anchor=N,
        text='%d Runs' % total_runs)

  def CreateHistogram(self, x_offset, y_offset, stats):
    """Create histogram of codelet run times.

    Args:
      x_offset: X-offset for Pie.
      y_offset: Y-offset for Pie.
      stats: Stats to display. Instance of
        :py:class:`~farg.core.run_stats.RunStats`.
    """
    all_runs = []
    for state, stats_for_state in stats.stats_per_state.items():
      all_runs.extend((state, x_offset)
                      for x_offset in stats_for_state.codelet_counts)
    all_runs = sorted(
        (x_offset for x_offset in all_runs if x_offset[1] > 0),
        key=lambda x_offset: x_offset[1])
    count = len(all_runs)
    if count == 0:
      return
    delta_x = kHistogramWidth / count
    max_codelet_count = max(x_offset[1] for x_offset in all_runs)
    for idx, run in enumerate(all_runs):
      color = StateToColor(run[0])
      y_end = y_offset + kHistogramHeight - kHistogramHeight * run[
          1] / max_codelet_count
      this_x = x_offset + delta_x * idx
      self.canvas.create_line(
          this_x, y_end, this_x, y_offset + kHistogramHeight, fill=color)
    self.canvas.create_text(
        x_offset + kHistogramWidth / 2,
        y_offset + kHistogramHeight + 10,
        anchor=N,
        text='Max codelets: %d' % max_codelet_count)

  def DisplayBasicStats(self, x_offset, y_offset, stats):
    """Display basic stats (mean run time, success rate, etc.) for one side.

    Args:
      x_offset: X-offset for Pie.
      y_offset: Y-offset for Pie.
      stats: Stats to display. Instance of
        :py:class:`~farg.core.run_stats.RunStats`.
    """
    successful_completion_stats = stats.stats_per_state[b'SuccessfulCompletion']
    total_runs = sum(
        len(x_offset.codelet_counts)
        for x_offset in stats.stats_per_state.values())
    if total_runs == 0:
      return
    percentage = '%3.2f%%' % (
        100 * len(successful_completion_stats.codelet_counts) / total_runs)
    self.canvas.create_text(
        x_offset, y_offset, anchor=NW, text='Success: %s' % percentage)
    codelet_counts = successful_completion_stats.codelet_counts
    if codelet_counts:
      mean_codelet_count = Mean(codelet_counts)
      median_codelet_count = Median(codelet_counts)
      self.canvas.create_text(
          x_offset,
          y_offset + 15,
          anchor=NW,
          text='Mean: %3.2f' % mean_codelet_count)
      self.canvas.create_text(
          x_offset,
          y_offset + 30,
          anchor=NW,
          text='Median: %3.2f' % median_codelet_count)

  def DisplayInferenceStats(self, stats, for_input, y):
    """Display inference stats: Is right hand side better than left?

    Args:
      stats: Instance of :py:class:`~farg.core.run_stats.AllStats`.
      for_input: What input string are we comparing the two sides?
      y: Y-offset of top of this display.
    """
    codelet_stats, success_stats = stats.GetComparitiveStats(for_input)
    if not codelet_stats or not success_stats:
      return
    self.canvas.create_text(
        10,
        y,
        anchor=NW,
        text='means: (%3.2f, %3.2f), variance: (%3.2f, %3.2f)' %
        (codelet_stats['left_mean'], codelet_stats['right_mean'],
         codelet_stats['left_variance'], codelet_stats['right_variance']))
    self.canvas.create_text(
        10,
        y + 20,
        anchor=NW,
        text='Counts: (%d, %d), k=%d, t=%3.2f, %s' %
        (codelet_stats['n1'], codelet_stats['n2'], codelet_stats['df'],
         codelet_stats['t'], codelet_stats['descriptor']))

    self.canvas.create_text(
        10,
        y + 40,
        anchor=NW,
        text='means: (%3.2f, %3.2f), variance: (%3.2f, %3.2f)' %
        (success_stats['left_mean'], success_stats['right_mean'],
         success_stats['left_variance'], success_stats['right_variance']))
    self.canvas.create_text(
        10,
        y + 60,
        anchor=NW,
        text='Counts: (%d, %d), k=%d, t=%3.2f, %s' %
        (success_stats['n1'], success_stats['n2'], success_stats['df'],
         success_stats['t'], success_stats['descriptor']))


class RunModeNonInteractive(RunMode):  # No init. pylint: disable=W0232
  """The RunMode that will start a GUI and start running the app multiple times."""

  @classmethod
  def DoSingleRun(cls, cmdline_arguments_list, extra_arguments=None):
    """Execute the application once.

    Args:
      cmdline_arguments_dict: Dictionary of arguments to pass process.
      extra_arguments: extra arguments that will be added, too.

    Returns:
      A string, representing output status and number of codelets.
    """
    arguments = []  # Collect arguments to pass to subprocess
    arguments.append(sys.executable)  # Python executable
    arguments.append(
        sys.argv[0])  # The script used to run this mode (e.g., run_seqsee.py)

    arguments.extend(cmdline_arguments_list)
    if extra_arguments:
      arguments.extend(extra_arguments)
    try:
      result = subprocess.check_output(arguments)
    except CalledProcessError as e:
      print(e)
      return 'ERROR'
    return result
