from farg.apps.pyseqsee.categorization.categorizable import Categorizable

class PSFocusable(Categorizable):
  def __init__(self):
    self.stored_fringe = None
    Categorizable.__init__(self)

  def GetFringe(self):
    fringe = self.CalculateFringe()
    for cat, instance_logic in self.categories.items():
      fringe[cat] = 1
      for att, val in instance_logic._attributes.items():
        fringe[(cat, att, val.Structure())] = 0.5
    self.stored_fringe = fringe
    return fringe

class PSStream(object):
  pass
