# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

import unittest

class CodeletPresenceSpec(object):
  def __init__(self, family, arguments=None):
    self.family = family
    if arguments:
      self.arguments = arguments
    else:
      self.arguments = dict()

class FringeAndCodeletsTest(unittest.TestCase):
  """Contains methods for testing the fringe of items."""

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

