class ViewPort(object):
  def __init__(self, canvas, left, bottom, width, height):
    self.left = left
    self.bottom = bottom
    self.height = height
    self.width = width
    self.canvas = canvas

  def ReDraw(self, controller):
    # Should delete things with particular identifiers. I will let canvas delete, for now.
    self.ReDrawView(controller)

  def CanvasCoordinates(self, x, y):
    return (self.left + x, self.bottom + y)
