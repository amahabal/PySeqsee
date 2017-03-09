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
"""Defines the base GUI for the GUI run-mode."""

import logging
import threading
from tkinter import Button, Frame, Label, StringVar, Tk
from tkinter.constants import LEFT
from tkinter.messagebox import askyesno, showinfo

from farg.core.exceptions import AnswerFoundException
from farg.core.ltm.manager import LTMManager
from farg.core.question.question import BooleanQuestion
from farg.core.ui.gui.central_pane import CentralPane
import farg.flags as farg_flags


class RunForNSteps(threading.Thread):
  """Runs controller for up to n steps.

  This does not update the GUI directly; It however results in changing the
  state of the
  attribute "controller" that it holds. This is shared by the GUI and used to
  update itself.

  Before each step, checks that we have not been asked to pause.
  """

  def __init__(self, *, controller, gui, num_steps=1000):
    threading.Thread.__init__(self)
    #: Controller for the whole app.
    self.controller = controller
    #: Number of steps taken so far.
    self.num_steps = num_steps
    #: GUI being displayed. We need this to communicate some state (such as "we have found
    #: an answer and can now quit.").
    self.gui = gui

  def run(self):  # Name stipulated by Thread. pylint: disable=C0103
    try:
      self.controller.RunUptoNSteps(self.num_steps)
    except AnswerFoundException:
      # We should exit.
      self.gui.quitting_called_from_thread = True
      return


class GUI:
  """Base-class of GUI for an application.

  Provides a :py:mod:`tkinter` based interface to display various components
  such as the workspace,
  and for interacting with the user (such as asking questions).

  **Supported Views**

  The central part of the window---everything except the row of buttons at the
  top---is controlled by
  an instance of the class
  :py:class:`~farg.core.ui.gui.central_pane.CentralPane` (see which for
  further details).The top-left corner of the window allows switching between
  different views.

  **Key Bindings**

  The UI allows running the app at various speeds---full steam ahead,
  step-by-step, or with long
  strides. These keyboard bindings are provided:

  * 'q' for Quit
  * 'c' for Continue (full-steam ahead!)
  * 'p' for Pause while running
  * 's' for Step (run one codelet)
  * 'l' for taking a 10-codelet stride
  * 'k' for taking a 100-codelet stride.
  """

  #: Size and location of the window.
  geometry = '1280x980-0+0'  # Not a const. pylint: disable=C6409

  #: Class handling the central part of the display.
  central_pane_class = CentralPane  # Not a const. pylint: disable=C6409

  def __init__(self, *, controller_class, stopping_condition_fn=None):
    self.run_state_lock = threading.Lock()
    self.pause_stepping = False
    self.quitting = False
    self.quitting_called_from_thread = False
    self.stepping_thread = None

    #: Button pane.
    self.buttons_pane = None  # Set up later.
    #: Central pane (a canvas).
    self.central_pane = None  # Set up later.
    #: A Tk variable tracking codelet count.
    self.codelet_count_var = None  # Set up later.

    self.controller = controller_class(
        ui=self, controller_depth=0, stopping_condition=stopping_condition_fn)
    self.mw = mw = Tk()
    # mw.geometry(self.geometry)

    self.mw.bind('<KeyPress-q>', lambda e: self.Quit())
    self.mw.bind('<KeyPress-s>', lambda e: self.StepsInAnotherThread(1))
    self.mw.bind('<KeyPress-l>', lambda e: self.StepsInAnotherThread(10))
    self.mw.bind('<KeyPress-k>', lambda e: self.StepsInAnotherThread(100))
    self.mw.bind('<KeyPress-c>', lambda e: self.StartThreaded())
    self.mw.bind('<KeyPress-p>', lambda e: self.Pause())

    self.items_to_refresh = []
    self.SetupWindows()
    self.RegisterQuestionHandlers()

  def UpdateDisplay(self):
    """Refresh the display. Erases everything and draws it again."""
    if self.quitting_called_from_thread:
      self.Quit()
    for item in self.items_to_refresh:
      try:
        item.ReDraw()
      except RuntimeError as error:
        # This may occur because the object being updated may have changed. Log a warning
        # and continue.
        logging.warn('Runtime error while updating: %s', error)
    self.codelet_count_var.set('%d' % self.controller.steps_taken)

  def SetupWindows(self):
    """Sets up frames in the GUI."""
    self.buttons_pane = Frame(self.mw)
    self.PopulateButtonPane(self.buttons_pane)
    self.buttons_pane.grid(row=0, column=0, columnspan=2)

    self.PopulateCentralPane()

  def StepsInAnotherThread(self, num_steps):
    with self.run_state_lock:
      if self.quitting:
        return
      if self.stepping_thread:
        if self.stepping_thread.is_alive():
          return
        else:
          self.stepping_thread = None
      self.stepping_thread = RunForNSteps(
          controller=self.controller, num_steps=num_steps, gui=self)
      self.pause_stepping = False
      self.stepping_thread.start()

  def StartThreaded(self):
    self.StepsInAnotherThread(10000)

  def Pause(self):
    with self.run_state_lock:
      self.pause_stepping = True
      if self.stepping_thread:
        self.stepping_thread.join()
        self.stepping_thread = None

  def Quit(self):
    """Called when quitting.

    Ensures that all threads have exited, and LTMs saved.
    """
    with self.run_state_lock:
      self.quitting = True
      self.pause_stepping = True
    self.Pause()
    self.mw.quit()
    LTMManager.SaveAllOpenLTMS()

  def PopulateButtonPane(self, frame):
    """Adds buttons to the top row."""
    Button(frame, text='Start', command=self.StartThreaded).pack(side=LEFT)
    Button(frame, text='Pause', command=self.Pause).pack(side=LEFT)
    Button(frame, text='Quit', command=self.Quit).pack(side=LEFT)
    self.codelet_count_var = StringVar()
    self.codelet_count_var.set('0')
    Label(
        frame,
        textvariable=self.codelet_count_var,
        font=('Helvetica', 28, 'bold')).pack(side=LEFT)

  def PopulateCentralPane(self):
    """Sets up the display in the central part.

    If an item must be refreshed, add it to items_to_refresh.
    """
    height = farg_flags.FargFlags.gui_canvas_height
    width = farg_flags.FargFlags.gui_canvas_width
    canvas = self.central_pane_class(
        self.mw,
        self.controller,
        height=int(height),
        width=int(width),
        background='#EEFFFF')
    canvas.grid(row=1, column=0)
    self.central_pane = canvas
    self.items_to_refresh.append(canvas)
    canvas.ReDraw()

  def PopulateInteractionPane(self):
    """Sets up the interaction pane at the bottom."""
    pass

  def AskQuestion(self, question):
    """Asks the question (by delegating to the Ask method of the question)."""
    return question.Ask(self)

  def RegisterQuestionHandlers(self):  # Needs to be a method. pylint: disable=R0201
    """Registers how to ask a given type of question."""

    def BooleanQuestionHandler(question, ui):  # pylint: disable=W0613
      return askyesno('', question.question_string)

    BooleanQuestion.Ask = BooleanQuestionHandler

  def DisplayMessage(self, message):  # Needs to be a method. pylint: disable=R0201
    showinfo('', message)
