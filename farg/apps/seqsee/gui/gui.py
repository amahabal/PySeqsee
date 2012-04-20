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

"""Adapting the generic FARG GUI to Seqsee."""

from farg.apps.seqsee.gui.groups_view import GroupsView
from farg.apps.seqsee.gui.workspace_view import WorkspaceView
from farg.core.ui.gui import GUI
from farg.core.ui.gui.central_pane import CentralPane
from farg.core.ui.gui.views.coderack_view import CoderackView
from farg.core.ui.gui.views.stream_view import StreamView
from farg.core.ui.gui.views.ltm_view import LTMView

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
       'ws_ltm_st':  lambda pane: pane.SetThreeWaySplit(WorkspaceView,
                                                       LTMView,
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

