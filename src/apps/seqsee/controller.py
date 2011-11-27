from farg.controller import Controller
from apps.seqsee.workspace import Workspace

class SeqseeController(Controller):
  def __init__(self):
    Controller.__init__(self)
    self.ws = Workspace()
