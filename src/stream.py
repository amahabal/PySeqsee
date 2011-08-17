class Stream(object):
  
  kRelatedItemThreshold = 0.01
  kDecayRatio = 0.95

  def __init__(self):
    self.foci = {}  # Maps foci to strength.
    self.stored_fringes = {}  # Maps fringe_elt to focus to strength map.

  def FociCount(self):
    return len(self.foci)
  
  def FocusOn(self, focusable):
    # If already stored, bring it to forefront
    if focusable in self.foci:
      self.foci.__delitem__(focusable)
      deletable_stored_fringe_items = []
      for k, v in self.stored_fringes.iteritems():
        v.__delitem__(focusable)
        if len(v) == 0:
          deletable_stored_fringe_items.append(k)
      for deletable in deletable_stored_fringe_items:
        self.stored_fringes.__delitem__(deletable)

    fringe = focusable.GetFringe()
    stored_fringe_map = self.stored_fringes
    hits_map = {}
    for k, v in fringe.iteritems():
      if k in stored_fringe_map:
        for related_focusable, strength in stored_fringe_map[k].iteritems():
          extra_strength = strength * self.foci[related_focusable] * v
          if extra_strength > self.kRelatedItemThreshold:
            if related_focusable in hits_map:
              hits_map[related_focusable] += extra_strength
            else:
              hits_map[related_focusable] = extra_strength
      if k in stored_fringe_map:
        stored_fringe_map[k][focusable] = v
      else:
        stored_fringe_map[k] = { focusable: v }
    for focus in self.foci.keys():
      self.foci[focus] *= self.kDecayRatio
    self.foci[focusable] = 1
    return hits_map