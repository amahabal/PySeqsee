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

    bigger_set_size = max(len(workspace.left_items), len(workspace.right_items))
    space_per_element = self.height / (bigger_set_size + 1)

    x_offset_for_left_set = self.width * 0.2
    x_offset_for_right_set = x_offset_for_left_set + self.width / 2

    for idx, element in enumerate(workspace.left_items):
      x, y = self.CanvasCoordinates(x_offset_for_left_set, (idx + 0.5) * space_per_element)
      self.canvas.create_text(
          x, y, text='%d' % element.magnitude,
          font='-adobe-helvetica-bold-r-normal--28-140-100-100-p-105-iso8859-4',
          fill='#0000FF')

    for idx, element in enumerate(workspace.right_items):
      x, y = self.CanvasCoordinates(x_offset_for_right_set, (idx + 0.5) * space_per_element)
      self.canvas.create_text(
          x, y, text='%d' % element.magnitude,
          font='-adobe-helvetica-bold-r-normal--28-140-100-100-p-105-iso8859-4',
          fill='#00FF00')
