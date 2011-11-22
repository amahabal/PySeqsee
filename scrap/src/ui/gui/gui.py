from Tkinter import Tk, Button, Canvas, Frame, Menu, TOP, LEFT
import sys
import ConfigParser

from ui.gui.central_pane import CentralPane
from ui.gui.conversation import Conversation

class GUI(object):
  """Tkinter-based UI for Seqsee."""

  def __init__(self, runstate):
    print "Will run GUI"
    config = ConfigParser.SafeConfigParser()
    config.read('config/gui.config')

    geometry = config.get('App', 'geometry')
    mw = Tk()
    mw.geometry(geometry)
    self.SetupWindows(mw, config, runstate)
    mw.mainloop()

  def SetupWindows(self, mw, config, runstate):
    button_frame = Frame(mw)
    button_frame.pack(side=TOP)
    self.SetupButtons(button_frame)

    central_pane_config = dict(config.items('CentralPane'))
    central_pane = self.central_pane = CentralPane(mw, **central_pane_config)
    central_pane.pack(side=TOP)

    conversation_config = dict(config.items('Conversation'))
    conversation = self.conversation = Conversation(mw, **conversation_config)
    conversation.pack(side=TOP)

    self.SetupBindings(mw)
    self.ReDraw(runstate)

  def ReDraw(self, runstate):
    self.conversation.ReDraw(runstate)
    self.central_pane.ReDraw(runstate)

  def SetupButtons(self, button_frame):
    Button(button_frame, text="Start", command=self.Start).pack(side=LEFT)
    Button(button_frame, text="Pause", command=self.Pause).pack(side=LEFT)
    Button(button_frame, text="Quit", command=self.Quit).pack(side=LEFT)

  def Start(self):
    """TODO FIXME: write this."""
    #TODO write this.
    pass

  def Pause(self):
    pass

  def Quit(self, *ignored):
    sys.exit(1)

  def SetupBindings(self, mw):
    mw.bind('<KeyPress-q>', self.Quit)
