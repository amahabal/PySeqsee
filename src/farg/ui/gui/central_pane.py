from tkinter import *
from third_party import gflags

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
