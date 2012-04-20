from farg.core.question.question import BooleanQuestion
from farg.core.ui.gui.central_pane import CentralPane
from farg.third_party import gflags
from tkinter import *
from tkinter.messagebox import askyesno
from tkinter.ttk import *
import logging
import threading

gflags.DEFINE_integer('gui_canvas_height', 500,
                      'Height of the central canvas')
gflags.DEFINE_integer('gui_canvas_width', 800,
                      'Width of the central canvas')

FLAGS = gflags.FLAGS

class RunForNSteps(threading.Thread):
  """Runs controller for upto n steps.
  
  Checking each time if we have not been asked to pause."""

  def __init__(self, *, controller, num_steps=1000):
    threading.Thread.__init__(self)
    self.controller = controller
    self.num_steps = num_steps

  def run(self):
    self.controller.RunUptoNSteps(self.num_steps)

class GUI:

  geometry = '810x700-0+0'
  central_pane_class = CentralPane

  def __init__(self, *, controller_class, stopping_condition_fn=None):
    self.run_state_lock = threading.Lock()
    self.pause_stepping = False
    self.quitting = False
    self.stepping_thread = None

    self.controller = controller_class(ui=self,
                                       controller_depth=0,
                                       stopping_condition=stopping_condition_fn)
    self.mw = mw = Tk()
    mw.geometry(self.geometry)

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
    for item in self.items_to_refresh:
      try:
        item.ReDraw()
      except RuntimeError as e:
        # This may occur because the object being updates may have changed. Log a warning
        # and continue.
        logging.warn('Runtime error while updating: %s' % e)
    self.codelet_count_var.set('%d' % self.controller.steps_taken)

  def SetupWindows(self):
    self.buttons_pane = Frame(self.mw)
    self.PopulateButtonPane(self.buttons_pane)
    self.buttons_pane.grid()

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
      self.stepping_thread = RunForNSteps(controller=self.controller, num_steps=num_steps)
      self.pause_stepping = False
      self.stepping_thread.start()

  def StartThreaded(self):
    self.StepsInAnotherThread(1000)

  def Pause(self):
    with self.run_state_lock:
      self.pause_stepping = True
      if self.stepping_thread:
        self.stepping_thread.join()
        self.stepping_thread = None

  def Quit(self):
    with self.run_state_lock:
      self.quitting = True
      self.pause_stepping = True
    self.Pause()
    self.mw.quit()

  def PopulateButtonPane(self, frame):
    """Adds buttons to the top row."""
    Button(frame, text="Start", command=self.StartThreaded).pack(side=LEFT)
    Button(frame, text="Pause", command=self.Pause).pack(side=LEFT)
    Button(frame, text="Quit", command=self.Quit).pack(side=LEFT)
    self.codelet_count_var = StringVar()
    self.codelet_count_var.set("0")
    Label(frame, textvariable=self.codelet_count_var,
          font='-adobe-helvetica-bold-r-normal--28-140-100-100-p-105-iso8859-4').pack(side=LEFT)

  def PopulateCentralPane(self):
    """Sets up the display in the central part.
    
    If an item must be refreshed, add it to items_to_refresh."""
    height = FLAGS.gui_canvas_height
    width = FLAGS.gui_canvas_width
    canvas = self.central_pane_class(self.mw, self.controller, FLAGS,
                                     height=height, width=width,
                                     background='#FEE')
    canvas.grid()
    self.central_pane = canvas
    self.items_to_refresh.append(canvas)
    canvas.ReDraw()

  def PopulateInteractionPane(self):
    """Sets up the interaction pane at the bottom."""
    pass

  def AskQuestion(self, question):
    return question.Ask(self)

  def RegisterQuestionHandlers(self):
    def boolean_question_handler(question, ui):
      return askyesno('', question.question_string)
    BooleanQuestion.Ask = boolean_question_handler
