from Tkinter import *
from apps.seqsee.gui.workspace_view import WorkspaceView
from apps.seqsee.gui.coderack_view import CoderackView

class CentralPane(Canvas):
  """The central pane of the Tk-based UI. This can hold several displays."""
  def __init__(self, master, controller, *args, **kwargs):
    self.height = int(kwargs['height'])
    self.width = int(kwargs['width'])
    self.controller = controller

    Canvas.__init__(self, master, **kwargs)
    self.SetupMenu(master)

    # Setup appropriate view based on config and commandline options.
    # Defaulting to full workspace view, for now.
    self.SetInitialView()

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

  def SetInitialView(self):
    self.SetVerticallySplitView(WorkspaceView, CoderackView)

  named_views = { 'ws': lambda pane: pane.SetFullView(WorkspaceView),
                  'cr': lambda pane: pane.SetFullView(CoderackView),
                  'ws_cr': lambda pane: pane.SetVerticallySplitView(WorkspaceView,
                                                                    CoderackView),
                 }
  def SetNamedView(self, name):
    CentralPane.named_views[name](self)

  def SetupMenu(self, parent):
    menubar = Menu(self)

    view_menu = Menu(menubar, tearoff=0)
    view_menu.add_command(label='workspace',
                          command=lambda: self.SetNamedView('ws'))
    view_menu.add_command(label='codelets',
                          command=lambda: self.SetNamedView('cr'))
    view_menu.add_command(label='ws/codelets',
                          command=lambda: self.SetNamedView('ws_cr'))
    menubar.add_cascade(label="View", menu=view_menu)

    parent.config(menu=menubar)
