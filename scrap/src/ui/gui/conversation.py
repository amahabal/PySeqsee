from Tkinter import *

class Conversation(Frame):
  def __init__(self, parent, *args, **kwargs):
    Frame.__init__(self, parent)
    text = self.text = Text(self, **kwargs)
    text.pack(side=LEFT)
    buttons_frame = Frame(self)
    buttons_frame.pack(side=RIGHT)

    self.buttons = []
    for pos in range(0, 4):
      self.buttons.append(
          Button(buttons_frame, text='', width=15, state='disabled'))
      self.buttons[-1].pack(side=TOP)

  def ReDraw(self, runstate):
    pass
