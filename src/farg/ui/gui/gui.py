from Tkinter import Tk, Button, Frame, Label, LEFT, TOP, StringVar, Toplevel, BOTTOM
from farg.exceptions import FargException, YesNoException
from farg.ui.gui.dot_to_graph import GraphViewer
from threading import Thread
import tkMessageBox

class RunForNSteps(Thread):
  """Runs controller for upto n steps.
  
  Checking each time if we have not been asked to pause."""

  def __init__(self, gui, n_steps=10000):
    Thread.__init__(self)
    self.gui = gui
    self.n_steps = n_steps

  def run(self):
    for _step in xrange(0, self.n_steps):
      if self.gui.stop_stepping:
        break
      try:
        self.gui.controller.Step()
        #print 'Finished step #%d' % self.gui.controller.steps_taken
      except FargException as e:
        self.gui.stop_stepping = True
        try:
          self.gui.HandleAppSpecificFargException(e)
        except FargException as f:
          self.gui.HandleFargException(f)
      if _step % 25 == 24:
        self.gui.ReDraw()
    self.gui.stepping_thread = None
    self.gui.ReDraw()

class GUI(object):
  """A tkinter-based interfact for a FARG app.
  
  It sets up three frames: a buttons frame, a central pane, and an interaction
  widget. Subclasses can override specific bits of it as needed."""

  def __init__(self, controller, args, geometry='810x700+0+0'):
    #: The main-window of the UI.
    self.mw = mw = Tk()
    #: The controller owned by the UI.
    self.controller = controller
    mw.geometry(geometry)
    self.SetupWindows(args)
    if args.gui_show_ltm:
      self.SetupLTMWindow(args)

    #: If non-None, the thread that is stepping the controller.
    self.stepping_thread = None

    #: If true, the stepping will stop after the next iteration.
    self.stop_stepping = False

  def Launch(self):
    """Starts the app by launching the UI."""
    self.mw.mainloop()

  def ReDraw(self):
    """Redraws the UI, flushing any changes that need to be."""
    for item in self.items_to_refresh:
      item.ReDraw()
    self.codelet_count_var.set('%d' % self.controller.steps_taken)

  def Quit(self):
    """Quits the application. Calls quit on the controller as well."""
    self.Pause()
    if self.stepping_thread:
      self.stepping_thread.join()
    self.controller.Quit()
    self.mw.quit()

  def Start(self):
    """Continually calls Step() on the controller."""
    if self.stepping_thread:
      return  # Already running.
    thread = RunForNSteps(self, n_steps=1000)
    if self.stepping_thread:
      return  # Already running.
    else:
      self.stepping_thread = thread
    self.stop_stepping = False
    thread.start()


  def Steps(self, steps):
    """Takes a single step of the controller."""
    if self.stepping_thread:
      return  # Already running.
    thread = RunForNSteps(self, n_steps=steps)
    if self.stepping_thread:
      return  # Already running.
    else:
      self.stepping_thread = thread
    self.stop_stepping = False
    thread.start()


  def Pause(self):
    """Pauses the stepping-through of the controller."""
    print "Pausing"
    self.stop_stepping = True

  def HandleAppSpecificFargException(self, exception):
    """A hook to allow derivative classes a way to handle specific types of exceptions.
    
    If unhandled, the exception should be rethrown.
    
    By default, this does nothing and rethrows the exception.
    """
    raise exception

  def HandleFargException(self, exception):
    """Takes care of the exception thrown by the controller, provided it is the right type."""
    try:
      raise exception
    except YesNoException:
      answer = tkMessageBox.askyesno("Question", exception.question_string)
      exception.callback(answer)

  def SetupWindows(self, args):
    """Sets up the three panes in the UI."""
    mw = self.mw
    self.items_to_refresh = []

    self.buttons_pane = Frame(mw)
    self.PopulateButtonPane(self.buttons_pane)
    self.buttons_pane.grid()

    self.PopulateCentralPane(args)
    self.PopulateInteractionPane(args)

  def SetupLTMWindow(self, args):
    """Creates a LTM-viewer window."""
    ltm_top = Toplevel()
    button_frame = Frame(ltm_top)
    button_frame.pack(side=TOP)
    Button(button_frame, text='Full Graph',
           command=lambda: self.graph_viewer.DrawGraph()).pack(side=LEFT)

    self.graph_viewer_message = StringVar()
    Label(ltm_top, textvariable=self.graph_viewer_message).pack(side=BOTTOM)
    self.graph_viewer_message.set("")

    graph_viewer = self.graph_viewer = GraphViewer(ltm_top, 400, 400, self.controller.ltm,
                                                   self.graph_viewer_message)
    graph_viewer.pack(side=TOP)
    graph_viewer.DrawGraph()
    self.items_to_refresh.append(graph_viewer)


  def PopulateButtonPane(self, frame):
    """Adds buttons to the top row."""
    Button(frame, text="Start", command=self.Start).pack(side=LEFT)
    Button(frame, text="Pause", command=self.Pause).pack(side=LEFT)
    Button(frame, text="Quit", command=self.Quit).pack(side=LEFT)
    self.codelet_count_var = StringVar()
    self.codelet_count_var.set("0")
    Label(frame, textvariable=self.codelet_count_var,
          font='-adobe-helvetica-bold-r-normal--28-140-100-100-p-105-iso8859-4',
          fg='#FF0000').pack(side=LEFT)

  def PopulateCentralPane(self):
    """Sets up the display in the central part.
    
    If an item must be refreshed, add it to items_to_refresh."""
    pass

  def PopulateInteractionPane(self):
    """Sets up the interaction pane at the bottom."""
    pass
