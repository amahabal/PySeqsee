import unittest
from apps.seqsee.workspace import Workspace
from apps.seqsee.controller import SeqseeController
from farg.controller import Controller
from farg.ltm.graph import LTMGraph
from apps.seqsee.anchored import SAnchored
from apps.seqsee.categories import Number
from apps.seqsee.mapping import NumericMapping

def HelperCreateAndInsertGroup(ws, specification, underlying_mapping=None):
  """Utility for quickly creating groups.

  Each element in the specification is a tuple consisting of integers or of other similarly
  structured tuples. Each generates a group, where the integers correspond to position in the
  workspace.

  A degenerate case is when the specification is an integer, in which case the WS element is
  returned.
  """
  if isinstance(specification, int):
    return ws.elements[specification]
  else:
    anchored_items = list(HelperCreateAndInsertGroup(ws, x) for x in specification)
    new_group = SAnchored.Create(*anchored_items, underlying_mapping=underlying_mapping)
    return ws.InsertGroup(new_group)

class MockSeqseeController(Controller):
  def __init__(self, items):
    Controller.__init__(self)
    ws = self.ws = Workspace()
    self.ltm = LTMGraph()
    ws.InsertElements(*items)

class CodeletPresenceSpec(object):
  def __init__(self, family, arguments=None):
    self.family = family
    if arguments:
      self.arguments = arguments
    else:
      self.arguments = dict()

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
    self.AssertCodeletsPresent(
        expected_similarity_affordances,
        list(prior_focus.GetSimilarityAffordances(
            other=current_focus,
            other_fringe=stream.stored_fringes[current_focus],
            my_fringe=stream.stored_fringes[prior_focus],
            controller=controller)))

  def AssertCodeletsPresent(self, specifications, container_to_check):
    """Checks for codelets with given specification in container_to_check, which is a list of
       codelets.

       Specifications is an iterable of individual specification, each of which is a
       CodeletPresenceSpec.
    """
    for codelet_presence_spec in specifications:
      self.AssertCodeletPresent(codelet_presence_spec, container_to_check)

  def AssertCodeletPresent(self, codelet_presence_spec, container_to_check):
    expected_family = codelet_presence_spec.family
    expected_arguments_dict = codelet_presence_spec.arguments
    for codelet in container_to_check:
      if codelet.family is not expected_family:
        continue
      arguments = codelet.args
      arguments_matched = True
      for argument, value in expected_arguments_dict.iteritems():
        if argument not in arguments:
          arguments_matched = False
          break
        if value != arguments[argument]:
          arguments_matched = False
          break
      if arguments_matched:
        return  # A matching codelet was found.
    # Nothing matched!
    self.fail("No codelet found matching family=%s where arguments contain %s" %
              (expected_family, expected_arguments_dict))



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

  def test_123_123(self):
    controller = MockSeqseeController((1, 2, 3, 1, 2, 3))
    ws = controller.ws
    numeric_succesor_mapping = NumericMapping('succ', Number)
    group1 = HelperCreateAndInsertGroup(ws, (0, 1, 2), numeric_succesor_mapping)
    group2 = HelperCreateAndInsertGroup(ws, (3, 4, 5), numeric_succesor_mapping)
    self.AssertFringeContains(controller, group1, { numeric_succesor_mapping: 0.9 })

    from apps.seqsee.get_mapping import CF_FindAnchoredSimilarity
    self.AssertFringeOverlap(
        controller, group1, group2, 0.4,
        expected_similarity_affordances=(
            CodeletPresenceSpec(CF_FindAnchoredSimilarity, {'left': group1,
                                                            'right': group2 }),))
