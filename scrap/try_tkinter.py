from tkinter import *

class Conversation(Frame):
  def __init__(self, parent, *args, **kwargs):
    Frame.__init__(self, parent, *args, **kwargs)
    buttons_frame = Frame(self)
    buttons_frame.pack(side=RIGHT)
    
    self.buttons = []
    for pos in range(0, 4):
      self.buttons.append(
          Button(text='', width=15, state='disabled'))
      self.buttons[-1].pack(side=TOP)
  def Fill(self):
    for button in self.buttons:
      button.configure(text="foo", state='active')

mw = Tk()
mw.geometry('810x700+0+0')

Label(mw, text="Hello, world!").pack()
c  = Conversation(mw)
c.pack(side=BOTTOM)

button_frame = Frame(mw)
button_frame.pack(side=TOP)

Button(button_frame, text='Quit', command=mw.quit).pack(side=LEFT)
Button(button_frame, text='Start', command=c.Fill).pack(side=LEFT)
Button(button_frame, text='Pause').pack(side=LEFT)

mw.mainloop()