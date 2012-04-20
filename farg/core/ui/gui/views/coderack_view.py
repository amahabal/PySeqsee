# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

from collections import defaultdict
from farg.core.ui.gui.views.list_based_view import ListBasedView
from tkinter import NW, Text, Toplevel
from tkinter.constants import END


def ShowCodeletFamilyDetails(controller, family):
  coderack = controller.coderack
  codelets = [x for x in coderack._codelets if x.family == family]
  top = Toplevel()
  tb = Text(top, height=50, width=50)
  tb.pack()
  for codelet in codelets:
    tb.insert(END, '%.1f\n' % codelet.urgency)
    for arg, val in codelet.args.items():
      tb.insert(END, '\t%s\t%s\n' % (arg, val))

class CoderackView(ListBasedView):

  def GetAllItemsToDisplay(self, controller):
    """Returns a 2-tuple: A top message, and a list of items."""
    coderack = controller.coderack
    families_to_urgency_sum = defaultdict(float)
    families_to_codelet_counts = defaultdict(int)
    total_codelets = 0
    total_urgency = 0
    for codelet in coderack._codelets:
      families_to_urgency_sum[codelet.family] += codelet.urgency
      families_to_codelet_counts[codelet.family] += 1
      total_codelets += 1
      total_urgency += codelet.urgency
    items = []
    for family, urgency in families_to_urgency_sum.items():
      items.append((family, urgency, families_to_codelet_counts[family]))
    message = '%d codelets from %d families.' % (total_codelets, len(items))
    return (items, message, dict(total_urgency=total_urgency))

  def DrawItem(self, widget_x, widget_y, item, extra_dict, controller):
    """Given x, y within the current widget and an item, draws it."""
    family, urgency, count = item
    total_urgency = extra_dict['total_urgency']
    urgency_fraction = 100.0 * urgency / total_urgency
    x, y = self.CanvasCoordinates(widget_x, widget_y)
    self.canvas.create_text(110 + x, y,
                            text='%2d %4.1f %s' % (count, urgency, family.__name__),
                            anchor=NW)
    rect_id = self.canvas.create_rectangle(x, y, x + urgency_fraction, y + 10,
                                           fill='#0000FF')
    self.canvas.tag_bind(rect_id, '<1>', lambda e: ShowCodeletFamilyDetails(controller,
                                                                            family))


