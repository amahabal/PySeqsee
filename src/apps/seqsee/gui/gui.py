"""Adapting the generic FARG GUI to Seqsee."""

from apps.seqsee.gui.conversation import Conversation
from farg.ui.gui import GUI
from third_party import gflags

gflags.DEFINE_string('gui_initial_view', 'ws',
                     'In GUI mode, what should the initial mode be?')
gflags.DEFINE_boolean('gui_show_ltm', False,
                      "Whether to show the LTM (it's expensive!)")

FLAGS = gflags.FLAGS

class SeqseeGUI(GUI):
  def __init__(self, **kwargs):
    GUI.__init__(self, **kwargs)
    self.mw.bind('<KeyPress-d>', lambda e: self.controller.workspace.DebugRelations())
