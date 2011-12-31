from apps.seqsee.workspace import Workspace
from apps.seqsee.codelet_families.read_from_ws import CF_ReadFromWS
from farg.controller import Controller

from farg.ltm.manager import LTMManager

kLTMName = 'seqsee.main'

def InitializeSeqseeLTM(ltm):
  """Called if ltm was empty (had no nodes)."""
  from apps.seqsee.sobject import SElement
  # Creates nodes for elements corresponding to the integers 1 through 10.
  element_nodes = []
  for magnitude in xrange(1, 11):
    element_nodes.append(ltm.GetNodeForContent(SElement(magnitude)))

LTMManager.RegisterInitializer(kLTMName, InitializeSeqseeLTM)

class SeqseeController(Controller):
  def __init__(self, args):
    routine_codelets_to_add = ((CF_ReadFromWS, 30, 0.3),)
    Controller.__init__(self, routine_codelets_to_add=routine_codelets_to_add,
                        ltm_name=kLTMName)
    ws = self.ws = Workspace()
    ws.InsertElements(*args.sequence)
    self.unrevealed_terms = args.unrevealed_terms
