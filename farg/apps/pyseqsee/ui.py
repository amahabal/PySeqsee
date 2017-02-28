from tkinter import LAST, NW, Toplevel, Text, END

from farg.core.exceptions import SuccessfulCompletion
from farg.core.question.question import BooleanQuestion
from farg.core.ui.batch_ui import BatchUI
from farg.core.ui.gui import GUI
from farg.core.ui.gui.central_pane import CentralPane
from farg.core.ui.gui.views.coderack_view import CoderackView
from farg.core.ui.gui.views.list_based_view import ListBasedView
from farg.core.ui.gui.views.ltm_view import LTMView
from farg.core.ui.gui.views.viewport import ViewPort
import farg.flags as farg_flags
class WorkspaceView(ViewPort):

  def __init__(self, canvas, left, bottom, width, height):
    ViewPort.__init__(self, canvas, left, bottom, width, height)
    self.elements_y = height * 0.5
    self.min_gp_height = height * 0.2
    self.max_gp_height = height * 0.4

  # Many local variables here.
  # pylint: disable=R0914
  def ReDraw(self, controller):
    workspace = controller.workspace
    revealed_terms = [x.magnitude for x in workspace.arena.element]
    space_per_element = self.width / (len(revealed_terms) + 1)

    for idx, element in enumerate(workspace.arena.element):
      x, y = self.CanvasCoordinates((idx + 0.5) * space_per_element,
                                    self.elements_y)
      self.canvas.create_text(
          x,
          y,
          text='%d' % element.magnitude,
          font='-adobe-helvetica-bold-r-normal--28-140-100-100-p-105-iso8859-4',
          fill='#0000FF')


class StreamView(ListBasedView):
  items_per_page = 5

  def GetAllItemsToDisplay(self, controller):
    """Returns a 2-tuple: A top message, and a list of items."""
    stream = controller.stream
    items_and_focus_time = stream.GetRecentFoci()
    return ([x[0] for x in items_and_focus_time], 'Stream', dict())

  def DrawItem(self, widget_x, widget_y, item, extra_dict, controller):
    """Given x, y within the current widget and an item, draws it."""
    x, y = self.CanvasCoordinates(widget_x, widget_y)
    text_id = self.canvas.create_text(x, y, text=item.BriefLabel(), anchor=NW)
    self.canvas.tag_bind(text_id, '<1>',
                         lambda e: self.ShowFocusableDetails(controller, item))
    fringe_strings = []
    for fringe_el, v in item.stored_fringe.items():
      if hasattr(fringe_el, 'BriefLabel'):
        fringe_strings.append((fringe_el.BriefLabel(), v))
      else:
        fringe_strings.append((str(fringe_el), v))
    fringe_string_for_item = '; '.join('%3.2f---%s' % (v, fringe_el)
                                       for fringe_el, v in fringe_strings)
    self.canvas.create_text(
        x + 5,
        y + 15,
        anchor=NW,
        text=fringe_string_for_item,
        width=self.width - widget_x - 5)

  def ShowFocusableDetails(self, controller, item):
    top = Toplevel()
    tb = Text(top, height=50, width=50)
    tb.pack()
    tb.insert(END, '%s\n\n' % item.BriefLabel())
    tb.insert(END, 'Show details...')


class PySeqseeCentralPane(CentralPane):
  default_initial_view = 'ws'
  named_views = {
      'ws':
          lambda pane: pane.SetFullView(WorkspaceView),
      'cr':
          lambda pane: pane.SetFullView(CoderackView),
      'ws_cr':
          lambda pane: pane.SetVerticallySplitView(WorkspaceView, CoderackView),
      'ws_cr_st':
          lambda pane: pane.SetThreeWaySplit(WorkspaceView, CoderackView, StreamView),
      'ws_cr_st_ltm':
          lambda pane: pane.SetFourWaySplit(WorkspaceView, CoderackView, StreamView, LTMView),
  }


class PySeqseeGUI(GUI):

  central_pane_class = PySeqseeCentralPane

  def __init__(self, *, controller_class, stopping_condition_fn=None):
    GUI.__init__(
        self,
        controller_class=controller_class,
        stopping_condition_fn=stopping_condition_fn)

    self.mw.title('PySeqsee')  #Sets the title of the window


def HasAsPrefix(longer_list, shorter_list):
  return longer_list[:len(shorter_list)] == shorter_list


class AreTheseTheNextTermsQuestion(BooleanQuestion):

  def __init__(self, terms):
    self.terms = terms
    BooleanQuestion.__init__(self, 'Are these the next few terms: %s?' % terms)


class PySeqseeBatchUI(BatchUI):

  def RegisterQuestionHandlers(self):

    def HandleNextTermsQuestion(question, ui):
      workspace = ui.controller.workspace
      current_known_terms = list(x.magnitude for x in workspace.arena.element)
      total_known_terms = farg_flags.FargFlags.sequence + farg_flags.FargFlags.unrevealed_terms
      expected_total_terms = current_known_terms + list(question.terms)
      if len(expected_total_terms) > len(total_known_terms):
        if (HasAsPrefix(expected_total_terms, total_known_terms)):
          raise SuccessfulCompletion(codelet_count=ui.controller.steps_taken)
        else:
          return False
      else:
        return HasAsPrefix(total_known_terms, expected_total_terms)

    AreTheseTheNextTermsQuestion.Ask = HandleNextTermsQuestion
