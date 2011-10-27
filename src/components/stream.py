from collections import defaultdict
class Stream(object):
  """Implements the Stream of Thought.
  
  Each episode of focusing on an object results in a fringe of it being remembered, and subsequent
  episodes may remind of prior episodes based on the degree of overlap of the fringes.
  """

  #: Minimum level of similarity to consider two episodes as potentially related.
  kRelatedItemThreshold = 0.01
  #: The factor by which the strength of a prior episode goes down each time a new episode is seen.
  kDecayRatio = 0.95
  #: Maximum number of focusables to keep around.
  kMaxFocusableCount = 10
  def __init__(self):
    #: Maps foci (i.e., things focused upon recently) to strength.
    self.foci = defaultdict(float)
    #: Maps fringe elements to a dict (which is a dict from focus to strength).
    self.stored_fringes = defaultdict(lambda: defaultdict(float))

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
    """Remove the focus that was added the most time ago --- it will have the least strength."""
    most_ancient_focus = min(self.foci, key=self.foci.get)
    self._RemovePriorFocus(most_ancient_focus)

  def FocusOn(self, focusable):
    """Focus on focusable, returning a hitmap: a map from previous focus to strength."""
    # If already stored, delete it. 
    if focusable in self.foci:
      self._RemovePriorFocus(focusable)

    if self.FociCount() == self.kMaxFocusableCount:
      self._RemoveMostAncientFocus()

    fringe = focusable.GetFringe()
    stored_fringe_map = self.stored_fringes
    hits_map = defaultdict(float)
    for k, v in fringe.iteritems():
      if k in stored_fringe_map:
        for related_focusable, strength in stored_fringe_map[k].iteritems():
          extra_strength = strength * self.foci[related_focusable] * v
          if extra_strength > self.kRelatedItemThreshold:
            hits_map[related_focusable] += extra_strength
      stored_fringe_map[k][focusable] = v
    for focus in self.foci.keys():
      self.foci[focus] *= self.kDecayRatio
    self.foci[focusable] = 1
    return hits_map
