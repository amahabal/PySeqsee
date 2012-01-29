import unittest
from apps.seqsee.workspace import Workspace
from apps.seqsee.controller import SeqseeController
from farg.controller import Controller
from farg.ltm.graph import LTMGraph

class MockSeqseeController(Controller):
  def __init__(self, items):
    Controller.__init__(self)
    ws = self.ws = Workspace()
    self.ltm = LTMGraph()
    ws.InsertElements(*items)

class FringeOverlapTest(unittest.TestCase):
  def SetupTestingWS(self, items):
    ws = Workspace()
    ws.InsertElements(*items)
    return ws

  def AssertFringeContains(self, controller, item, expected_fringe_components):
    """Checks for the presence of particular components in the fringe.
  
       Args:
         item: The item whose fringe is being tested.
         expected_fringe_components: An iterable of two-tuples (fringe element and minimum
             intensity)).
    """
    fringe = item.GetFringe(controller)
    for fringe_element, min_expected_intensity in expected_fringe_components.iteritems():
      self.assertTrue(fringe_element in fringe,
                      'Fringe element %s in fringe' % fringe_element)
      actual_intensity = fringe[fringe_element]
      self.assertTrue(actual_intensity >= min_expected_intensity,
                      'Actual intensity (%f) for %s is less than minimum expected (%f)' %
                           (actual_intensity, fringe_element, min_expected_intensity))

  def AssertFringeOverlap(self, controller, prior_focus, current_focus, min_expected_overlap,
                          expected_similarity_affordances):
    """Checks that the fringes of two items overlap and have certain similarity affordances.
    
    Args:
      controller: controller that contains the stream, LTM and so forth.
      prior_focus: The previous focus in the stream (will have intensity 1)
      current_focus: The current item being focused upon.
      min_expected_overlap: Minimum expected overlap between the fringes.
      expected_similarity_affordances: what codelets are expected? This is specified as a
          iterable of codelet-matchers (that is, as family, min_urgency, max_urgency,
          and some required arguments, or a subset thereof).
    """
    stream = controller.stream
    stream.Clear()
    stream._StoreFringeAndCalculateOverlap(prior_focus)
    hits_map = stream._StoreFringeAndCalculateOverlap(current_focus)
    self.assertTrue(prior_focus in hits_map,
                    "Expected overlap of fringes of %s and %s" % (prior_focus,
                                                                  current_focus))
    self.assertTrue(hits_map[prior_focus] >= min_expected_overlap,
                    "Fringe overlap between %s and %s lower (%f) than expected (%f)" %
                    (prior_focus, current_focus, hits_map[prior_focus],
                     min_expected_overlap))
    # TODO(# --- Jan 29, 2012): Finish this, test similarity affordances.

class FringeOverlapTestForAnchored(FringeOverlapTest):
  def test_sanity(self):
    controller = MockSeqseeController(range(0, 10))
    ws = controller.ws
    item_at_pos_1 = ws.GetItemAt(1, 1)
    item_1_node = controller.ltm.GetNodeForContent(item_at_pos_1.object)
    self.AssertFringeContains(controller, item_at_pos_1, {'pos:1': 0.5,
                                                          'pos:2': 0.3,
                                                          item_1_node: 0.4,
                                                          })

    item_at_pos_2 = ws.GetItemAt(2, 2)
    self.AssertFringeOverlap(controller,
                             prior_focus=item_at_pos_1,
                             current_focus=item_at_pos_2,
                             min_expected_overlap=0.3,
                             expected_similarity_affordances=())
