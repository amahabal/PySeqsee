"""Adapting the generic FARG GUI to Seqsee."""

from Tkinter import Canvas, TOP
from farg.ui.gui import gui

class SeqseeGUI(gui.GUI):
  def PopulateCentralPane(self, frame):
    canvas = Canvas(frame, height=300, width=500, background='#F00')
    canvas.pack(side=TOP)
    self.ws_canvas = canvas
    self.items_to_refresh.append(self.controller.runstate.ws)
