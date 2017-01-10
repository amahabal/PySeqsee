from farg.core.ui.gui.views.viewport import ViewPort
from tkinter import LAST, NW

class WorkspaceView(ViewPort):
  def __init__(self, canvas, left, bottom, width, height):
    ViewPort.__init__(self, canvas, left, bottom, width, height)

  def ReDraw(self, controller):
    """Redraw the workspace if it is being displayed. This is not called otherwise.

    The attributes that you have access to include self.width, self.height and a method to
    convert this widget's coordinates to the full canvas coordinates.
    """
    workspace = controller.workspace

    # EDIT-ME: You'd want to add something real here.
    x, y = self.CanvasCoordinates(10, 10)
    self.canvas.create_text(x, y, text='Hello, World!', anchor=NW)
