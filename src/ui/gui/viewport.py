class ViewPort(object):
  def __init__(self, canvas, left, bottom, width, height, identifier):
    self.left = left
    self.bottom = bottom
    self.height = height
    self.width = width
    self.canvas = canvas
    self.identifier = identifier

  def ReDraw(self, run_state):
    # Should delete things with identifers. I will let canvas delete, for now.
    print "Will redraw viewport"
    self.ReDrawView(run_state)

  def CanvasCoordinates(self, x, y):
    return (self.left + x, self.bottom + y)
