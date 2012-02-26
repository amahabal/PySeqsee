# Base class of UIs (including GUIs, cmdline, and other versions).

from threading import Thread
from farg.exceptions import FargException

class RunForNSteps(Thread):
  """Runs controller for upto n steps.
  
  Checking each time if we have not been asked to pause."""

  def __init__(self, ui, n_steps=10000):
    Thread.__init__(self)
    self.gui = ui
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
    self.gui.ReDraw()
    self.gui.stepping_thread = None


class UI(object):

  def __init__(self, controller, flags):
    self.controller = controller
    controller.ui = self

    self.flags = flags


