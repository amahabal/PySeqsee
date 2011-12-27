from apps.seqsee.gui.viewport import ViewPort
from collections import defaultdict
from math import ceil
from Tkinter import NW

class CoderackView(ViewPort):
  families_per_page = 5

  def __init__(self, canvas, left, bottom, width, height, identifier):
    ViewPort.__init__(self, canvas, left, bottom, width, height, identifier)
    self.height_per_row = 0.8 * (height - 20) / CoderackView.families_per_page
    self.current_page_number = 1

  def ReDrawView(self, controller):
    coderack = controller.coderack
    families_to_urgency_sum = defaultdict(float)
    families_to_codelet_counts = defaultdict(int)
    total_codelets = 0
    for codelet in coderack._codelets:
      families_to_urgency_sum[codelet.family] += codelet.urgency
      families_to_codelet_counts[codelet.family] += 1
      total_codelets += 1
    families_count = len(families_to_codelet_counts)
    max_page_number = ceil(1.0 * families_count / CoderackView.families_per_page)
    if self.current_page_number > max_page_number:
      self.current_page_number = 1
    index_of_first_family = (self.current_page_number - 1) * CoderackView.families_per_page
    index_beyond_last_family = index_of_first_family + CoderackView.families_per_page
    if index_beyond_last_family > families_count:
      index_beyond_last_family = families_count
    families_to_show = families_to_codelet_counts.keys()[index_of_first_family:index_beyond_last_family]

    message = '%d codelets from %d families. Page %d of %d' % (
        total_codelets, families_count, self.current_page_number, max_page_number)
    x, y = self.CanvasCoordinates(0, 0)
    self.canvas.create_text(x, y, text=message, anchor=NW)

    row_top_y = 20
    for family in families_to_show:
      count = families_to_codelet_counts[family]
      urgency = '%4.1f' % families_to_urgency_sum[family]
      x, y = self.CanvasCoordinates(20, row_top_y)
      self.canvas.create_text(x, y, text='%2d %s %s' % (count, urgency, family),
                              anchor=NW)
      row_top_y += self.height_per_row
