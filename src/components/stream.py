# TODO(#4 --- Dec 28, 2011): Move to src/farg.
from collections import defaultdict
from apps.seqsee.util import WeightedChoice, ChooseAboutN

class Stream(object):
  """Implements the Stream of Thought.
  
  Each episode of focusing on an object results in a fringe of it being remembered, and
  subsequent episodes may remind of prior episodes based on the degree of overlap of the
  fringes.
  """

  #: Minimum level of similarity to consider two episodes as potentially related.
  kRelatedItemThreshold = 0.01
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

  def FociCount(self):
    """Counts the number of recent items focused upon."""
    return len(self.foci)


  def _RemovePriorFocus(self, focusable):
    """Remove a previous focus (and any fringe elements solely supported by that focus."""
    self.foci.__delitem__(focusable)
    deletable_stored_fringe_items = []
    for k, v in self.stored_fringes.iteritems():
      if focusable in v:
        v.__delitem__(focusable)
        if len(v) == 0:
          deletable_stored_fringe_items.append(k)

    for deletable in deletable_stored_fringe_items:
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
    self._PrepareForFocusing(focusable)
    hit_map = self._CalculateFringeOverlap(focusable)
    if not hit_map:
      return

    # Possibly add codelets based on the fringe hit.
    potential_codelets = []
    for prior_focusable, overlap_amount in hit_map.iteritems():
      if overlap_amount < 0.1:
        continue
      potential_codelets.extend(prior_focusable.GetSimilarityAffordances(
          focusable,
          other_fringe=self.stored_fringes[focusable],
          my_fringe=self.stored_fringes[prior_focusable],
          controller=self.controller))

    potential_codelets.extend(focusable.GetAffordances(controller=self.controller))
    if potential_codelets:
      selected_codelets = ChooseAboutN(2, [(x, x.urgency) for x in potential_codelets])
      for one_codelet in selected_codelets:
        self.controller.coderack.AddCodelet(one_codelet)

  def _CalculateFringeOverlap(self, focusable):
    """Calculates a hit map: from prior focusable to strength."""
    fringe = focusable.GetFringe()
    stored_fringe_map = self.stored_fringes
    hits_map = defaultdict(float)
    for fringe_element, intensity in fringe.iteritems():
      if fringe_element in stored_fringe_map:
        for related_focusable, strength in stored_fringe_map[fringe_element].iteritems():
          extra_strength = strength * self.foci[related_focusable] * intensity
          if extra_strength > self.kRelatedItemThreshold:
            hits_map[related_focusable] += extra_strength
      stored_fringe_map[fringe_element][focusable] = intensity
    for focus in self.foci.keys():
      self.foci[focus] *= self.kDecayRatio
    self.foci[focusable] = 1
    return hits_map
