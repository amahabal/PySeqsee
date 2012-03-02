from apps.seqsee.codelet_families.read_from_ws import CF_ReadFromWS
from apps.seqsee.workspace import Workspace
from farg.controller import Controller
from farg.ltm.manager import LTMManager
from farg.ltm.edge import LTMEdge
from apps.seqsee.codelet_families.all import CF_RemoveSpuriousRelations

kLTMName = 'seqsee.main'

def InitializeSeqseeLTM(ltm):
  """Called if ltm was empty (had no nodes)."""
  from apps.seqsee.sobject import SElement
  # Creates nodes for elements corresponding to the integers 1 through 10.
  elements = [SElement(magnitude) for magnitude in xrange(1, 11)]
  for element in elements:
    ltm.GetNodeForContent(element)
  for idx, element in enumerate(elements[:-1]):
    ltm.AddEdgeBetweenContent(element, elements[idx + 1],
                              LTMEdge.LTM_EDGE_TYPE_RELATED)
    ltm.AddEdgeBetweenContent(elements[idx + 1], element,
                              LTMEdge.LTM_EDGE_TYPE_RELATED)
  from apps.seqsee.categories import Prime, Squares, TriangularNumbers
  for prime_number in (2, 3, 5, 7):
    ltm.AddEdgeBetweenContent(elements[prime_number - 1], Prime(),
                              LTMEdge.LTM_EDGE_TYPE_ISA)
#  for square in Squares.number_list[:10]:
#    ltm.AddEdgeBetweenContent(SElement(square), Squares(), LTMEdge.LTM_EDGE_TYPE_ISA)
#  for triangular in TriangularNumbers.number_list[:10]:
#    ltm.AddEdgeBetweenContent(SElement(triangular), TriangularNumbers(),
#                              LTMEdge.LTM_EDGE_TYPE_ISA)


LTMManager.RegisterInitializer(kLTMName, InitializeSeqseeLTM)

class SeqseeController(Controller):
  def __init__(self, flags):
    routine_codelets_to_add = ((CF_ReadFromWS, 30, 0.3),
                               (CF_RemoveSpuriousRelations, 30, 0.1))
    Controller.__init__(self, routine_codelets_to_add=routine_codelets_to_add,
                        ltm_name=kLTMName)
    ws = self.ws = self.workspace = Workspace()
    ws.InsertElements(*flags.sequence)
    self.unrevealed_terms = flags.unrevealed_terms
