from collections import defaultdict
from Tkinter import NW, Text, Toplevel

from apps.seqsee.gui.list_based_view import ListBasedView
from Tkconstants import END

def ShowCodeletFamilyDetails(controller, family):
  coderack = controller.coderack
  codelets = [x for x in coderack._codelets if x.family == family]
  top = Toplevel()
  tb = Text(top, height=50, width=50)
  tb.pack()
  for codelet in codelets:
    tb.insert(END, '%.1f\n' % codelet.urgency)
    for arg, val in codelet.args.iteritems():
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
    for family, urgency in families_to_urgency_sum.iteritems():
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


