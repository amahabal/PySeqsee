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

  def SetupMenu(self, parent):
    menubar = Menu(self)

    view_menu = Menu(menubar, tearoff=0)
    view_menu.add_command(label='workspace',
                          command=lambda: self.SetFullView(WorkspaceView))
    view_menu.add_command(label='codelets',
                          command=lambda: self.SetFullView(CoderackView))
    view_menu.add_command(label='ws/codelets',
                          command=lambda: self.SetVerticallySplitView(WorkspaceView,
                                                                      CoderackView))
    menubar.add_cascade(label="View", menu=view_menu)

    parent.config(menu=menubar)
