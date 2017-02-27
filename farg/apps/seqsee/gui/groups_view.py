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
from tkinter import NW, Text, Toplevel
from tkinter.constants import END

from farg.core.ui.gui.views.list_based_view import ListBasedView
def ShowGroupDetails(controller, group):
  top = Toplevel()
  tb = Text(top, height=50, width=50)
  tb.pack()
  tb.insert(END, str(group) + "\n")
  tb.insert(END, "======= Relations\n")
  for rel in group.relations:
    other_end = rel.first if rel.second == group else rel.second
    tb.insert(END, "\n%s\n" % other_end)
    for mapping in rel.mapping_set:
      tb.insert(END, "\t%s\n" % mapping)
  tb.insert(END, "\n======= Categories \n")
  for cat, binding in group.object.categories.items():
    tb.insert(END, "\nCategory %s ==>\n" % str(cat))
    for key, val in binding.bindings.items():
      tb.insert(END, "\t%s --> %s\n" % (key, str(val)))

class GroupsView(ListBasedView):

  def GetAllItemsToDisplay(self, controller):
    """Returns a 2-tuple: A top message, and a list of items."""
    workspace = controller.workspace
    items = [x for x in workspace.groups]
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
    categories_string = '; '.join(x.BriefLabel() for x in gp.object.categories.keys())
    self.canvas.create_text(x + 5, y + 15, anchor=NW, text=categories_string)

