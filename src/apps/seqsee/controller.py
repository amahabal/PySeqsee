from apps.seqsee.codelet_families.read_from_ws import CF_ReadFromWS
from apps.seqsee.workspace import Workspace
from farg.ltm.manager import LTMManager
from farg.ltm.edge import LTMEdge
from apps.seqsee.codelet_families.all import CF_RemoveSpuriousRelations

from third_party import gflags
from farg.controller import Controller
import sys
FLAGS = gflags.FLAGS

gflags.DEFINE_float('seqsee_remove_spurious_relation_probability',
                    0.1,
                    'Probability of adding a codelet to clean relations. '
                    'This is a useless flag to test the SxS system. Should be removed')

kLTMName = 'seqsee.main'

def InitializeSeqseeLTM(ltm):
  """Called if ltm was empty (had no nodes)."""
  from apps.seqsee.sobject import SElement
  # Creates nodes for elements corresponding to the integers 1 through 10.
  elements = [SElement(magnitude) for magnitude in range(1, 11)]
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
  routine_codelets_to_add = ((CF_ReadFromWS, 30, 0.3),
                             (CF_RemoveSpuriousRelations, 10000,
                              FLAGS.seqsee_remove_spurious_relation_probability))
  workspace_class = Workspace
  ltm_name = kLTMName

  def __init__(self, **args):
    Controller.__init__(self, **args)
    self.routine_codelets_to_add = ((CF_ReadFromWS, 30, 0.3),
                                    (CF_RemoveSpuriousRelations, 30,
                                     FLAGS.seqsee_remove_spurious_relation_probability))
    self.workspace.InsertElements(*FLAGS.sequence)
    self.unrevealed_terms = FLAGS.unrevealed_terms
