"""Adapting the generic FARG GUI to Bongard."""

from farg.apps.bongard.gui.workspace_view import WorkspaceView
from farg.core.ui.gui import GUI
from farg.core.ui.gui.central_pane import CentralPane
from farg.core.ui.gui.views.coderack_view import CoderackView
from farg.core.ui.gui.views.stream_view import StreamView
class BongardCentralPane(CentralPane):
  default_initial_view = 'ws'
  named_views = {
      'ws': lambda pane: pane.SetFullView(WorkspaceView),
      'cr': lambda pane: pane.SetFullView(CoderackView),
      'ws_cr': lambda pane: pane.SetVerticallySplitView(WorkspaceView, CoderackView),
      'cr_st':  lambda pane: pane.SetVerticallySplitView(CoderackView, StreamView),
      'ws_cr_st':  lambda pane: pane.SetThreeWaySplit(WorkspaceView,
                                                      CoderackView,
                                                      StreamView),
      # EDIT-ME: Add other combinations of views as needed.
      }

class BongardGUI(GUI):

  central_pane_class = BongardCentralPane

  def __init__(self, **kwargs):
    GUI.__init__(self, **kwargs)
    self.mw.title("Bongard")
    # EDIT-ME: You may wish to add key-bindings.
  

