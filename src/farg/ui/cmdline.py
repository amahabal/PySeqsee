from farg.ui.ui import UI

class CmdlineUI(UI):
  """A non-gui UI."""

  def __init__(self, controller):
    UI.__init__(self, controller)

  def Launch(self):
    """Starts the app by launching the UI."""
    self.Steps(5000)

  def DisplayMessage(self, message):
    print '[%d] Message: %s' % (self.controller.steps_taken, message)

  def AskYesNoQuestion(self, question):
    print '[%d] Question: %s' % (self.controller.steps_taken, question)
    ans = raw_input('[y/n] ').lower().find('y') >= 0
    print "You chose %s" % ans
    return ans
