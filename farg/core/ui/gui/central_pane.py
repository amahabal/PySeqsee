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

from farg.third_party import gflags
from tkinter import *

gflags.DEFINE_string('gui_initial_view', '',
                     'In GUI mode, what should the initial mode be?')
FLAGS = gflags.FLAGS

class CentralPane(Canvas):
  """The central pane of the Tk-based UI. This can hold several displays."""

  named_views = {}
  default_initial_view = ''

  def __init__(self, master, controller, seqsee_args, *args, **kwargs):
    self.height = int(kwargs['height'])
    self.width = int(kwargs['width'])
    self.controller = controller
    self.viewports = []
    Canvas.__init__(self, master, **kwargs)
    self.SetupMenu(master)
    self.SetNamedView(FLAGS.gui_initial_view or self.default_initial_view)

  def ReDraw(self):
    self.delete(ALL)
    for viewport in self.viewports:
      viewport.ReDraw(self.controller)

  def SetFullView(self, view_class):
    self.viewports = [view_class(self, 0, 0, self.width, self.height)]
    self.ReDraw()

  def SetVerticallySplitView(self, view_class1, view_class2):
    self.viewports = [view_class1(self, 0, 0, self.width, self.height / 2 - 2),
                      view_class2(self, 0, self.height / 2 + 2,
                                  self.width, self.height / 2 - 2)]
    self.ReDraw()

  def SetThreeWaySplit(self, view_class1, view_class2, view_class3):
    self.viewports = [view_class1(self, 0, 0, self.width, self.height / 2 - 2),
                      view_class2(self, 0, self.height / 2 + 2,
                                  self.width / 2 - 2, self.height / 2 - 2),
                      view_class3(self, self.width / 2 + 2, self.height / 2 + 2,
                                  self.width / 2 - 2, self.height / 2 - 2)]
    self.ReDraw()

  def SetNamedView(self, name):
    self.named_views[name](self)

  def NamedViewCmd(self, name):
    return (lambda: self.SetNamedView(name))

  def SetupMenu(self, parent):
    menubar = Menu(self)

    view_menu = Menu(menubar, tearoff=0)
    for name in list(self.named_views.keys()):
      view_menu.add_command(label=name,
                            command=self.NamedViewCmd(name))
    menubar.add_cascade(label="View", menu=view_menu)

    debug_menu = Menu(menubar, tearoff=0)
    debug_menu.add_command(label='Debug Relations',
                           command=lambda: self.controller.workspace.DebugRelations())
    menubar.add_cascade(label="Debug", menu=debug_menu)
    parent.config(menu=menubar)
