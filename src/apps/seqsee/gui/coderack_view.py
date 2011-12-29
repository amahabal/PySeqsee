from collections import defaultdict
from Tkinter import NW

from apps.seqsee.gui.list_based_view import ListBasedView

class CoderackView(ListBasedView):

  def GetAllItemsToDisplay(self, controller):
    """Returns a 2-tuple: A top message, and a list of items."""
    coderack = controller.coderack
    families_to_urgency_sum = defaultdict(float)
    families_to_codelet_counts = defaultdict(int)
    total_codelets = 0
    for codelet in coderack._codelets:
      families_to_urgency_sum[codelet.family] += codelet.urgency
      families_to_codelet_counts[codelet.family] += 1
      total_codelets += 1
    items = []
    for family, urgency in families_to_urgency_sum.iteritems():
      items.append((family, urgency, families_to_codelet_counts[family]))
    message = '%d codelets from %d families.' % (total_codelets, len(items))
    return (items, message)

  def DrawItem(self, widget_x, widget_y, item):
    """Given x, y within the current widget and an item, draws it."""
    family, urgency, count = item
    x, y = self.CanvasCoordinates(widget_x, widget_y)
    self.canvas.create_text(x, y, text='%2d %4.1f %s' % (count, urgency, family.__name__),
                            anchor=NW)


