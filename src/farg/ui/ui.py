# Base class of UIs (including GUIs, cmdline, and other versions).

from threading import Thread
from third_party import gflags

FLAGS = gflags.FLAGS

class RunForNSteps(Thread):
  """Runs controller for upto n steps.
  
  Checking each time if we have not been asked to pause."""

  def __init__(self, ui, n_steps=10000):
    Thread.__init__(self)
    self.ui = ui
    self.n_steps = n_steps

  def run(self):
    for _step in xrange(0, self.n_steps):
      if self.ui.stop_stepping:
        break
      self.ui.controller.Step()
      if _step % 25 == 24:
        self.ui.ReDraw()
    self.ui.ReDraw()
    self.ui.stepping_thread = None


class UI(object):

  def __init__(self, controller):
    self.controller = controller
    controller.ui = self

    #: If non-None, the thread that is stepping the controller.
    self.stepping_thread = None

    #: If true, the stepping will stop after the next iteration.
    self.stop_stepping = False

    #: If true, the process of quitting has started.
    self.quitting = False

  def Quit(self):
    """Quits the application. Calls quit on the controller as well."""
    self.Pause()
    self.quitting = True
    stepping_thread = self.stepping_thread
    if stepping_thread:
      try:
        stepping_thread.join(2)
      except AttributeError:  # The thread already gone.
        pass
    self.controller.Quit()
    self.CleanupAfterQuit()

  def CleanupAfterQuit(self):
    pass

  def StartThreaded(self):
    """Continually calls Step() on the controller."""
    self.StepsInAnotherThread(1000)


  def StepsInAnotherThread(self, steps):
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

  def Steps(self, steps):
    for _step in xrange(0, steps):
      self.controller.Step()

  def Pause(self):
    """Pauses the stepping-through of the controller."""
    print "Pausing"
    self.stop_stepping = True

  def ReDraw(self):
    """Called to update visual state (especially for GUIs)."""
    pass

  def DisplayMessage(self, message):
    """Should be implemented by individual UIs to display a message."""
    pass

  def AskYesNoQuestion(self, question):
    """Should be implemented by individual UIs to display a boolean question."""
    raise NotImplementedError("Should have been implemented by subclass")
