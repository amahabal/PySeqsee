"""Adapting the generic FARG GUI to Seqsee."""

from apps.seqsee.gui.central_pane import CentralPane
from apps.seqsee.gui.conversation import Conversation
from third_party import gflags
from tide.ui.gui import GUI

gflags.DEFINE_string('gui_initial_view', 'ws',
                     'In GUI mode, what should the initial mode be?')
gflags.DEFINE_integer('gui_canvas_height', 400,
                      'Height of the central canvas')
gflags.DEFINE_integer('gui_canvas_width', 800,
                      'Width of the central canvas')
gflags.DEFINE_boolean('gui_show_ltm', False,
                      "Whether to show the LTM (it's expensive!)")

FLAGS = gflags.FLAGS

class SeqseeGUI(GUI):
  def __init__(self, **kwargs):
    GUI.__init__(self, **kwargs)

    self.mw.bind('<KeyPress-q>', lambda e: self.Quit())
    self.mw.bind('<KeyPress-s>', lambda e: self.StepsInAnotherThread(1))
    self.mw.bind('<KeyPress-l>', lambda e: self.StepsInAnotherThread(10))
    self.mw.bind('<KeyPress-k>', lambda e: self.StepsInAnotherThread(100))
    self.mw.bind('<KeyPress-c>', lambda e: self.StartThreaded())
    self.mw.bind('<KeyPress-p>', lambda e: self.Pause())
    self.mw.bind('<KeyPress-d>', lambda e: self.controller.workspace.DebugRelations())

  def PopulateCentralPane(self):
    height = FLAGS.gui_canvas_height
    width = FLAGS.gui_canvas_width
    canvas = CentralPane(self.mw, self.controller, FLAGS,
                         height=height, width=width,
                         background='#FEE')
    canvas.grid()
    self.central_pane = canvas
    self.items_to_refresh.append(canvas)
    canvas.ReDraw()

  def PopulateInteractionPane(self):
    conversation = Conversation(self.mw, self.controller, height=10)
    conversation.grid()
    self.conversation = conversation
    self.items_to_refresh.append(conversation)
    conversation.ReDraw()
