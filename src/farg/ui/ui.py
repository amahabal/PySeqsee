# Base class of UIs (including GUIs, cmdline, and other versions).

class UI(object):

  def __init__(self, controller, flags):
    self.controller = controller
    controller.ui = self

    self.flags = flags


