from apps.seqsee.gui.viewport import ViewPort

class WorkspaceView(ViewPort):
  def __init__(self, canvas, left, bottom, width, height):
    ViewPort.__init__(self, canvas, left, bottom, width, height)
    self.elements_y = height * 0.5
    self.min_gp_height = height * 0.2
    self.max_gp_height = height * 0.4

  def ReDrawView(self, controller):
    ws = controller.ws
    revealed_terms = [x.object.magnitude for x in ws.elements]
    space_per_element = self.width / (len(revealed_terms) + 1)
    for idx, term in enumerate(revealed_terms):
      x, y = self.CanvasCoordinates((idx + 0.5) * space_per_element,
                                     self.elements_y)
      self.canvas.create_text(x, y, text='%d' % term)