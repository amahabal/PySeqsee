from farg.run_state import RunState
from apps.seqsee.workspace import Workspace
from components.coderack import Coderack
from components.stream import Stream

class SeqseeRunState(RunState):
  def __init__(self):
    RunState.__init__(self)
    self.ws = Workspace()
    self.coderack = Coderack(20)
    self.stream = Stream()
