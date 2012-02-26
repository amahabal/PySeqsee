# Base class of UIs (including GUIs, cmdline, and other versions).

from threading import Thread
from farg.exceptions import FargException

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
      try:
        self.ui.controller.Step()
        #print 'Finished step #%d' % self.gui.controller.steps_taken
      except FargException as e:
        self.ui.stop_stepping = True
        try:
          self.ui.HandleAppSpecificFargException(e)
        except FargException as f:
          self.ui.HandleFargException(f)
      if _step % 25 == 24:
        self.ui.ReDraw()
    self.ui.ReDraw()
    self.ui.stepping_thread = None


class UI(object):

  def __init__(self, controller, flags):
    self.controller = controller
    controller.ui = self

    self.flags = flags

    #: If non-None, the thread that is stepping the controller.
    self.stepping_thread = None

    #: If true, the stepping will stop after the next iteration.
    self.stop_stepping = False

  def Quit(self):
    """Quits the application. Calls quit on the controller as well."""
    self.Pause()
    if self.stepping_thread:
      self.stepping_thread.join()
    self.controller.Quit()
    self.CleanupAfterQuit()

  def CleanupAfterQuit(self):
    pass

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

  def ReDraw(self):
    """Called to update visual state (especially for GUIs)."""
    pass
