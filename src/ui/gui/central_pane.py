from Tkinter import *

class CentralPane(Canvas):
  def __init__(self, parent, *args, **kwargs):
    Canvas.__init__(self, parent, **kwargs)
    self.SetupMenu(parent)

  def ReDraw(self, run_state):
    pass

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
