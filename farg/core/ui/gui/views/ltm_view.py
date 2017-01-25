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

"""View for displaying nodes in an ltm."""

from farg.core.ui.gui.views.list_based_view import ListBasedView
from tkinter import END, NW, Text, Toplevel

def ShowNodeDetails(controller, node):
  top = Toplevel()
  tb = Text(top, height=50, width=50)
  tb.pack()
  tb.insert(END, '%s\n\n' % node.content.BriefLabel())
  for edge in node.outgoing_edges:
    tb.insert(END,
              '{%s} -- %5.3f \t %s\n' % (', '.join(edge.edge_type_set),
                                         edge.utility,
                                         edge.to_node.content.BriefLabel()))

class LTMView(ListBasedView):
  """View for displaying nodes in an ltm."""

  items_per_page = 10

  def GetAllItemsToDisplay(self, controller):
    """A list of things to display.

    Args:
      controller: Controller for the application.

    Returns:
      A 3-tuple: Items, a top message, and a dictionary of extra information. The extra
        information is the number of timesteps taken in the ltm.
    """
    ltm = controller.ltm
    items_with_activations = []
    epoch = controller.steps_taken
    for node in ltm.nodes:
      items_with_activations.append((node, node.GetActivation(epoch)))
    items = sorted(items_with_activations, reverse=True, key=lambda x: x[1])
    message = ''
    return (items, message, dict(epoch=epoch))

  def DrawItem(self, widget_x, widget_y, item, extra_dict, controller):
    """Given x, y within the current widget and an item, draws it."""
    node, activation = item
    x, y = self.CanvasCoordinates(widget_x, widget_y)
    text_id = self.canvas.create_text(20 + x, y,
                                      text='%1.3f [Ab: %05d] %s' % (activation, node.abundance,
                                                                    node.content.BriefLabel()),
                                      anchor=NW)
    self.canvas.tag_bind(text_id, '<1>', lambda e: ShowNodeDetails(controller, node))
