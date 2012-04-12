"""Adapting the generic FARG GUI to Seqsee."""

from apps.seqsee.gui.coderack_view import CoderackView
from apps.seqsee.gui.groups_view import GroupsView
from apps.seqsee.gui.stream_view import StreamView
from apps.seqsee.gui.workspace_view import WorkspaceView
from farg.ui.gui import GUI
from third_party import gflags
from farg.ui.gui.central_pane import CentralPane

gflags.DEFINE_boolean('gui_show_ltm', False,
                      "Whether to show the LTM (it's expensive!)")

FLAGS = gflags.FLAGS

class SeqseeCentralPane(CentralPane):
  default_initial_view = 'ws'
  named_views = {
      'ws': lambda pane: pane.SetFullView(WorkspaceView),
      'cr': lambda pane: pane.SetFullView(CoderackView),
      'ws_cr': lambda pane: pane.SetVerticallySplitView(WorkspaceView, CoderackView),
      'cr_st':  lambda pane: pane.SetVerticallySplitView(CoderackView, StreamView),
      'ws_cr_st':  lambda pane: pane.SetThreeWaySplit(WorkspaceView,
                                                      CoderackView,
                                                      StreamView),
       'ws_gr_st':  lambda pane: pane.SetThreeWaySplit(WorkspaceView,
                                                       GroupsView,
                                                       StreamView),
       }

class SeqseeGUI(GUI):

  central_pane_class = SeqseeCentralPane

  def __init__(self, **kwargs):
    GUI.__init__(self, **kwargs)

    # Key bindings
    self.mw.bind('<KeyPress-d>', lambda e: self.controller.workspace.DebugRelations())

