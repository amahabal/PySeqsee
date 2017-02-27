from farg.apps.pyseqsee.categorization.categorizable import Categorizable
from farg.core.history import History


class PSFocusable(Categorizable):

  def __init__(self):
    self.stored_fringe = None
    History.Note("Focusable created")
    Categorizable.__init__(self)

  def GetFringe(self):
    fringe = self.CalculateFringe()
    for cat, instance_logic in self.categories.items():
      fringe[cat] = 1
      for att, val in instance_logic._attributes.items():
        fringe[(cat, att, val.Structure())] = 0.5
    self.stored_fringe = fringe
    History.Note("GetFringe called")
    return fringe

  def GetActions(self):
    return []

  def GetRemindingBasedActions(self, prior_overlapping):
    return []
