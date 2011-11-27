"""Adapting the generic FARG GUI to Seqsee."""

from Tkinter import Canvas, TOP
from farg.ui.gui import gui
from apps.seqsee.gui.central_pane import CentralPane
from apps.seqsee.gui.conversation import Conversation

class SeqseeGUI(gui.GUI):
  def __init__(self, controller, geometry='810x700+0+0'):
    gui.GUI.__init__(self, controller, geometry)
    self.mw.bind('<KeyPress-q>', self.Quit)

  def PopulateCentralPane(self):
    canvas = CentralPane(self.mw, height=400, width=800, background='#FEE')
    canvas.grid()
    self.central_pane = canvas
    self.items_to_refresh.append(canvas)
    canvas.ReDraw(self.controller)

  def PopulateInteractionPane(self):
    conversation = Conversation(self.mw, height=10)
    conversation.grid()
    self.conversation = conversation
    self.items_to_refresh.append(conversation)
