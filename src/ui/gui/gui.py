from Tkinter import Tk, Button, Canvas, Frame, TOP, LEFT
import sys

import ConfigParser

class GUI(object):
  """Tkinter-based UI for Seqsee."""

  def __init__(self, run_state):
    print "Will run GUI"
    config = ConfigParser.SafeConfigParser()
    config.read('config/gui.config')

    geometry = config.get('App', 'geometry')
    mw = Tk()
    mw.geometry(geometry)
    self.SetupWindows(mw, config, run_state)
    mw.mainloop()

  def SetupWindows(self, mw, config, run_state):
    button_frame = Frame(mw)
    button_frame.pack(side=TOP)
    self.SetupButtons(button_frame)

    canvas_config = dict(config.items('Canvas'))
    canvas = self.canvas = Canvas(mw, **canvas_config)
    canvas.pack(side=TOP)

    self.SetupBindings(mw)

  def SetupButtons(self, button_frame):
    Button(button_frame, text="Start", command=self.Start).pack(side=LEFT)
    Button(button_frame, text="Pause", command=self.Pause).pack(side=LEFT)
    Button(button_frame, text="Quit", command=self.Quit).pack(side=LEFT)

  def Start(self):
    pass

  def Pause(self):
    pass

  def Quit(self, *ignored):
    sys.exit(1)

  def SetupBindings(self, mw):
    mw.bind('<KeyPress-q>', self.Quit)
