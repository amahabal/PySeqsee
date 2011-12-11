from apps.seqsee.workspace import Workspace
from apps.seqsee.codelet_families.read_from_ws import CF_ReadFromWS
from farg.controller import Controller

class SeqseeController(Controller):
  def __init__(self, args):
    routine_codelets_to_add = ((CF_ReadFromWS, 30, 0.3),)
    Controller.__init__(self, routine_codelets_to_add=routine_codelets_to_add,
                        ltm_name='seqsee.main')
    ws = self.ws = Workspace()
    ws.InsertElements(*args.sequence)
    self.unrevealed_terms = args.unrevealed_terms
