from collections import defaultdict
from tkinter import NW, Text, Toplevel

from apps.seqsee.gui.list_based_view import ListBasedView
from tkinter.constants import END

def ShowGroupDetails(controller, group):
  top = Toplevel()
  tb = Text(top, height=50, width=50)
  tb.pack()
  tb.insert(END, str(group) + "\n")
  for rel in group.relations:
    tb.insert(END, "Reln: %s\n" % rel)

class GroupsView(ListBasedView):

  def GetAllItemsToDisplay(self, controller):
    """Returns a 2-tuple: A top message, and a list of items."""
    ws = controller.ws
    items = [x for x in ws.groups]
    message = '%d groups.' % (len(items))
    return (items, message, dict())

  def DrawItem(self, widget_x, widget_y, item, extra_dict, controller):
    """Given x, y within the current widget and an item, draws it."""
    gp = item
    x, y = self.CanvasCoordinates(widget_x, widget_y)
    gp_widget_id = self.canvas.create_text(x, y,
                                           text=str(gp),
                                           anchor=NW)
    self.canvas.tag_bind(gp_widget_id, '<1>',
                         lambda e: ShowGroupDetails(controller,
                                                    gp))


