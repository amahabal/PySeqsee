from apps.seqsee.gui.viewport import ViewPort
from collections import defaultdict
from math import ceil
from Tkinter import NW

class CoderackView(ViewPort):
  families_per_page = 5

  def __init__(self, canvas, left, bottom, width, height):
    ViewPort.__init__(self, canvas, left, bottom, width, height)
    self.height_per_row = 0.8 * (height - 20) / CoderackView.families_per_page
    self.current_page_number = 1

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
    self.canvas.create_text(x, y, text='%2d %4.1f %s' % (count, urgency, family),
                            anchor=NW)


  def ReDrawView(self, controller):
    items, top_message = self.GetAllItemsToDisplay(controller)
    families_count = len(items)
    max_page_number = ceil(1.0 * families_count / CoderackView.families_per_page)
    if self.current_page_number > max_page_number:
      self.current_page_number = 1
    index_of_first_family = (self.current_page_number - 1) * CoderackView.families_per_page
    index_beyond_last_family = index_of_first_family + CoderackView.families_per_page
    if index_beyond_last_family > families_count:
      index_beyond_last_family = families_count
    items_to_show = items[index_of_first_family:index_beyond_last_family]
    x, y = self.CanvasCoordinates(0, 0)
    self.canvas.create_text(x, y, text=top_message, anchor=NW)

    row_top_y = 20
    for item in items_to_show:
      self.DrawItem(20, row_top_y, item)
      row_top_y += self.height_per_row
