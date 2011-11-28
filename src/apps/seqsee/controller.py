from apps.seqsee.workspace import Workspace
from farg.controller import Controller

class SeqseeController(Controller):
  def __init__(self, args):
    Controller.__init__(self)
    ws = self.ws = Workspace()
    ws.InsertElements(*args.sequence)
    self.unrevealed_terms = args.unrevealed_terms
