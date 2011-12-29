from collections import defaultdict
from Tkinter import NW

from apps.seqsee.gui.list_based_view import ListBasedView

class StreamView(ListBasedView):

  items_per_page = 3

  def GetAllItemsToDisplay(self, controller):
    """Returns a 2-tuple: A top message, and a list of items."""
    stream = controller.stream
    items = sorted(stream.foci.items(), reverse=True, key=lambda item: item[1])
    return (items, 'Stream: %d prior foci' % len(stream.foci))

  def DrawItem(self, widget_x, widget_y, item):
    """Given x, y within the current widget and an item, draws it."""
    focus, strength = item
    x, y = self.CanvasCoordinates(widget_x, widget_y)
    self.canvas.create_text(x, y, text='%2.3f %s' % (strength, focus),
                            anchor=NW)


