# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

from tkinter import *

class Conversation(Frame):
  def __init__(self, master, controller, *args, **kwargs):
    Frame.__init__(self, master)
    self.controller = controller
    text = self.text = Text(self, **kwargs)
    text.pack(side=LEFT)
    buttons_frame = Frame(self)
    buttons_frame.pack(side=RIGHT)

    self.buttons = []
    for _pos in range(0, 4):
      self.buttons.append(
          Button(buttons_frame, text='', width=15, state='disabled'))
      self.buttons[-1].pack(side=TOP)

  def ReDraw(self):
    pass
