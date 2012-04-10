# Utility functions for testing seqsee.
from apps.seqsee.anchored import SAnchored
from apps.seqsee.workspace import Workspace
from farg.ltm.graph import LTMGraph
import unittest
from farg.controller import Controller

class MockSeqseeController(Controller):
  def __init__(self, items):
    Controller.__init__(self, ui=None)
    workspace = self.workspace = Workspace()
    self.ltm = LTMGraph()
    workspace.InsertElements(*items)

class CodeletPresenceSpec(object):
  def __init__(self, family, arguments=None):
    self.family = family
    if arguments:
      self.arguments = arguments
    else:
      self.arguments = dict()

# Too many public methods because of unittest. pylint: disable=R0904
class FringeOverlapTest(unittest.TestCase):

  @staticmethod
  def HelperCreateAndInsertGroup(workspace, specification, underlying_mapping=None):
    """Utility for quickly creating groups.

       Each element in the specification is a tuple consisting of integers or of other
       similarly structured tuples. Each generates a group, where the integers correspond to
       position in the workspace.

       A degenerate case is when the specification is an integer, in which case the WS
       element is returned.
    """
    if isinstance(specification, int):
      return workspace.elements[specification]
    else:
      anchored_items = list(FringeOverlapTest.HelperCreateAndInsertGroup(workspace, x)
                            for x in specification)
      new_group = SAnchored.Create(*anchored_items, underlying_mapping=underlying_mapping)
      return workspace.InsertGroup(new_group)

  @staticmethod
  def SetupTestingWS(items):
    workspace = Workspace()
    workspace.InsertElements(*items)
    return workspace

  def AssertFringeContains(self, controller, item, expected_fringe_components):
    """Checks for the presence of particular components in the fringe.

       Args:
         item: The item whose fringe is being tested.
         expected_fringe_components: An iterable of two-tuples (fringe element and minimum
             intensity)).
    """
    fringe = item.GetFringe(controller)
    for fringe_element, min_expected_intensity in expected_fringe_components.items():
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
    stream.StoreFringeAndCalculateOverlap(prior_focus)
    hits_map = stream.StoreFringeAndCalculateOverlap(current_focus)
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
    """Check if codelet matching spec is present in a list of codelets."""
    expected_family = codelet_presence_spec.family
    expected_arguments_dict = codelet_presence_spec.arguments
    for codelet in container_to_check:
      if codelet.family is not expected_family:
        continue
      arguments = codelet.args
      arguments_matched = True
      for argument, value in expected_arguments_dict.items():
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
