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

# TODO(#4 --- Dec 28, 2011): Move to src/farg.
from collections import defaultdict
from farg.core.focusable_mixin import FocusableMixin
from farg.core.util import ChooseAboutN

class Stream(object):
  """Implements the Stream of Thought.

     The main public function here is FocusOn(), called with::
       
       stream.FocusOn(focusable)
       
     where focusable must be an instance of the interface FocusableMixin. FocusableMixin
     defines three methods: GetFringe(), GetAffordances(), and GetSimilarityAffordances().
     
     The net effect of the call to FocusOn is to influence future processing in two ways:
     
       * By adding codelets, as described below.
       * By modifying the context in which future FocusOn()s work. This is implicit in the
         description of GetSimilarityAffordances() below.
         
     A blow-by-blow account of what happens:
     
       * The fringe of the focusable is obtained via a call to GetFringe().
       * If this fringe overlaps a prior stored fringe sufficiently, 
         GetSimilarityAffordances() is called on the prior focusable and can create codelets,
         but not just yet add these to the coderack.
       * GetAffordances() may generate more codelets that haven't yet been added.
       * Of these potential codelets, about 2 are chosen (biased by urgency) for addition to
         the coderack.
  """

  #: Minimum level of similarity to consider two episodes as potentially related.
  kRelatedItemThreshold = 0.01
  #: Minimum overlap with previous focusable to trigger GetSimilarityAffordances()
  kMinOverlapToTriggerSimilarity = 0.1
  #: The factor by which the strength of a prior episode goes down each time a new episode
  #: is seen.
  kDecayRatio = 0.95
  #: Maximum number of focusables to keep around.
  kMaxFocusableCount = 10
  def __init__(self, controller):
    #: Maps foci (i.e., things focused upon recently) to strength.
    self.foci = defaultdict(float)
    #: Maps fringe elements to a dict (which is a dict from focus to strength).
    self.stored_fringes = defaultdict(lambda: defaultdict(float))
    #: Controller for the stream (needed to take fringe-hit based actions)
    self.controller = controller

  def Clear(self):
    """Clears all state."""
    self.stored_fringes.clear()
    self.foci.clear()

  def FociCount(self):
    """Counts the number of recent items focused upon."""
    return len(self.foci)


  def _RemovePriorFocus(self, focusable):
    """Remove a previous focus (and any fringe elements solely supported by that focus."""
    self.foci.__delitem__(focusable)
    deletable_stored_fringe_elts = []
    for fringe_element, focus_to_strength_dict in self.stored_fringes.items():
      if focusable in focus_to_strength_dict:
        focus_to_strength_dict.__delitem__(focusable)
        if len(focus_to_strength_dict) == 0:
          deletable_stored_fringe_elts.append(fringe_element)

    for deletable in deletable_stored_fringe_elts:
      self.stored_fringes.__delitem__(deletable)

  def _RemoveMostAncientFocus(self):
    """Remove the focus with the least strength."""
    most_ancient_focus = min(self.foci, key=self.foci.get)
    self._RemovePriorFocus(most_ancient_focus)

  def _PrepareForFocusing(self, focusable):
    """Does legwork for focusing; if focusable is a recent focus, removes it."""
    # If already stored, delete it. 
    if focusable in self.foci:
      self._RemovePriorFocus(focusable)

    if self.FociCount() == self.kMaxFocusableCount:
      self._RemoveMostAncientFocus()

  def FocusOn(self, focusable):
    """Focus on focusable, and act on a fringe-hit."""
    assert(isinstance(focusable, FocusableMixin))
    focusable.OnFocus(self.controller)
    self._PrepareForFocusing(focusable)
    hit_map = self.StoreFringeAndCalculateOverlap(focusable)
    if not hit_map:
      return

    # Possibly add codelets based on the fringe hit.
    potential_codelets = []
    for prior_focusable, overlap_amount in hit_map.items():
      if overlap_amount < Stream.kMinOverlapToTriggerSimilarity:
        continue
      potential_codelets.extend(prior_focusable.GetSimilarityAffordances(
          focusable,
          other_fringe=self.stored_fringes[focusable],
          my_fringe=self.stored_fringes[prior_focusable],
          controller=self.controller))

    potential_codelets.extend(focusable.GetAffordances(controller=self.controller))
    if potential_codelets:
      selected_codelets = ChooseAboutN(2, [(x, x.urgency) for x in potential_codelets])
      for codelet in selected_codelets:
        self.controller.coderack.AddCodelet(codelet)

  def StoreFringeAndCalculateOverlap(self, focusable):
    """Calculates a hit map: from prior focusable to strength."""
    fringe = focusable.GetFringe(self.controller)
    stored_fringe_map = self.stored_fringes
    hits_map = defaultdict(float)
    for fringe_element, intensity in fringe.items():
      if fringe_element in stored_fringe_map:
        for related_focusable, strength in stored_fringe_map[fringe_element].items():
          extra_strength = strength * self.foci[related_focusable] * intensity
          if extra_strength > self.kRelatedItemThreshold:
            hits_map[related_focusable] += extra_strength
      stored_fringe_map[fringe_element][focusable] = intensity
    for focus in list(self.foci.keys()):
      self.foci[focus] *= self.kDecayRatio
    self.foci[focusable] = 1
    return hits_map
