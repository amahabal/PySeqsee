from tkinter.constants import END
from tkinter import NW, Text, Toplevel
from apps.seqsee.gui.list_based_view import ListBasedView
from collections import defaultdict


def ShowFocusableDetails(controller, focusable):
  stream = controller.stream
  stored_fringes = stream.stored_fringes
  top = Toplevel()
  tb = Text(top, height=50, width=50)
  tb.pack()
  tb.insert(END, '%s\n\n' % focusable)
  for fringe_element, strength_dict in stored_fringes.items():
    if focusable in strength_dict:
      tb.insert(END, '%.1f\t%s\n' % (strength_dict[focusable], fringe_element))


class StreamView(ListBasedView):

  items_per_page = 3

  def GetAllItemsToDisplay(self, controller):
    """Returns a 2-tuple: A top message, and a list of items."""
    stream = controller.stream
    items = sorted(list(stream.foci.items()), reverse=True, key=lambda item: item[1])
    return (items, 'Stream: %d prior foci' % len(stream.foci), dict())

  def DrawItem(self, widget_x, widget_y, item, extra_dict, controller):
    """Given x, y within the current widget and an item, draws it."""
    focus, strength = item
    x, y = self.CanvasCoordinates(widget_x, widget_y)
    text_id = self.canvas.create_text(x, y, text='%2.3f %s' % (strength, focus),
                                      anchor=NW)
    self.canvas.tag_bind(text_id, '<1>', lambda e: ShowFocusableDetails(controller,
                                                                        focus))


