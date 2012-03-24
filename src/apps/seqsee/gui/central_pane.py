from tkinter import *
from apps.seqsee.gui.coderack_view import CoderackView
from apps.seqsee.gui.groups_view import GroupsView
from apps.seqsee.gui.stream_view import StreamView
from apps.seqsee.gui.workspace_view import WorkspaceView

class CentralPane(Canvas):
  """The central pane of the Tk-based UI. This can hold several displays."""
  def __init__(self, master, controller, seqsee_args, *args, **kwargs):
    self.height = int(kwargs['height'])
    self.width = int(kwargs['width'])
    self.controller = controller

    Canvas.__init__(self, master, **kwargs)
    self.SetupMenu(master)

    # Setup appropriate view based on config and commandline options.
    # Defaulting to full workspace view, for now.
    self.SetNamedView(seqsee_args.gui_initial_view)

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

  named_views = { 'ws': lambda pane: pane.SetFullView(WorkspaceView),
                  'cr': lambda pane: pane.SetFullView(CoderackView),
                  'ws_cr': lambda pane: pane.SetVerticallySplitView(WorkspaceView,
                                                                    CoderackView),
                  'cr_st':  lambda pane: pane.SetVerticallySplitView(CoderackView,
                                                                     StreamView),
                  'ws_cr_st':  lambda pane: pane.SetThreeWaySplit(WorkspaceView,
                                                                  CoderackView,
                                                                  StreamView),
                  'ws_gr_st':  lambda pane: pane.SetThreeWaySplit(WorkspaceView,
                                                                  GroupsView,
                                                                  StreamView),
                 }
  def SetNamedView(self, name):
    CentralPane.named_views[name](self)

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
