from Tkinter import Tk, Button, Canvas, Frame, TOP, LEFT
import sys

class GUI(object):
  """Tkinter-based UI for Seqsee."""
  
  def __init__(self, run_state):
    print "Will run GUI"
    
    mw = Tk()
    mw.geometry('810x700+0+0')
    self.SetupWindows(mw, run_state)
    mw.mainloop()

  def SetupWindows(self, mw, run_state):
    button_frame = Frame(mw)
    button_frame.pack(side=TOP)
    Button(button_frame, text="Quit", command=self.Quit).pack(side=LEFT)
    canvas = self.canvas = Canvas(mw, width=800, height=600,
                                  bg='#EEEEFF')
    canvas.pack(side=TOP)

  def Quit(self):
    sys.exit(1)