"""The workspace is the virtual blackboard on which various codelets make annotations.
"""

from farg.core.categorization.categorizable import CategorizableMixin
from farg.core.ltm.storable import LTMStorableMixin
from farg.core.meta import MemoizedConstructor

class PlatonicInteger(LTMStorableMixin, metaclass=MemoizedConstructor):
  """Integer in long-term memory.

  Holds an integer that can be stored in LTM (and about which we can store information such as
  remembered categories."""

  def __init__(self, magnitude):
    self.magnitude = magnitude

  def BriefLabel(self):
    return 'Platonic %d' % self.magnitude

class IntegerObject(CategorizableMixin, LTMStorableMixin):
  """Holds one item in either set, along with any book-keeping information."""
  
  def __init__(self, magnitude):
    self.magnitude = magnitude

  def GetLTMStorableContent(self):
    return PlatonicInteger(self.magnitude)

class BongardWorkspace:
  """The top-level workspace for Bongard.

  Subspaces may define their own workspaces."""

  def __init__(self):
    self.left_items = []
    self.right_items = []
    
  def SetItems(self, left_magnitudes, right_magnitudes):
    for magnitude in left_magnitudes:
      self.left_items.append(IntegerObject(magnitude))
    for magnitude in right_magnitudes:
      self.right_items.append(IntegerObject(magnitude))
    print("Set up the items!")

