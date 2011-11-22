from Tkinter import *
from ui.gui.workspace_view import WorkspaceView

class CentralPane(Canvas):
  def __init__(self, parent, *args, **kwargs):
    height = int(kwargs['height'])
    width = int(kwargs['width'])

    Canvas.__init__(self, parent, **kwargs)
    self.SetupMenu(parent)

    # Setup appropriate view based on config and commandline options.
    # Defaulting to full workspace view, for now.
    self.SetInitialView(width, height)

  def ReDraw(self, runstate):
    self.delete(ALL)
    for viewport in self.viewports:
      viewport.ReDraw(runstate)

  def SetInitialView(self, width, height):
    self.viewports = [WorkspaceView(self, 0, 0, width, height, "ws")]

  def SetViewCmdFactory(self, view_name):
    # TODO write function 
    def CreatedFn():
      print "Will switch to view %s" % view_name
    return CreatedFn

  def SetupMenu(self, parent):
    menubar = Menu(self)

    view_menu = Menu(menubar, tearoff=0)
    view_menu.add_command(label='codelets',
                          command=self.SetViewCmdFactory('foo'))
    menubar.add_cascade(label="View", menu=view_menu)

    parent.config(menu=menubar)
