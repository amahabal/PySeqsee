from farg.core.ltm.storable import LTMNodeContent, LTMStorableMixin
from farg.core.categorization.categorizable import CategorizableMixin
from farg.core.focusable_mixin import FocusableMixin


class PlatonicObject(LTMNodeContent):
  """A stringified representation of a structure---i.e., of possibly nested tuples of integers.

  PlatonicObject are cached, meaning that with the same constructor argument, we always get the same
  object back.
  """

  def __init__(self, *, rep):
    assert(isinstance(rep, str))
    self.rep = rep

  @classmethod
  def CreateFromStructure(cls, structure):
    """Create a PlatonicObject. Structure can be an integer, or a tuple of structures.

    Note that (4,) is NOT the same as (((4,),),)."""
    return cls(rep=cls._StructureToString(structure))

  @classmethod
  def _StructureToString(cls, structure):
    if isinstance(structure, int):
      return str(structure)
    assert(isinstance(structure, tuple))
    return '(' + ', '.join(cls._StructureToString(x) for x in structure) + ')'


class PSObject(LTMStorableMixin, CategorizableMixin):
  """Represents an element or group in the workspace.

  This may be anchored or not. When anchored, it has a start and end offset.

  TODO(amahabal): Yet to fill in the notion of anchoring and offsets.

  TODO(amahabal): Have not yet ported over the code for getting the fringe and strength.

  TODO(amahabal): Also not present yet is the storage of relations.
  """

  def __init__(self):
    self.is_anchored = False

  def GetStorable(self):
    return PlatonicObject.CreateFromStructure(self.Structure())


class PSElement(PSObject):
  """Represents a single element in the sequence."""

  def __init__(self, *, magnitude):
    PSObject.__init__(self)
    self.magnitude = magnitude

  def Structure(self):
    return self.magnitude


class PSGroup(PSObject):
  """Represents a group, including the degenerate case of singleton or empty group.

  TODO(amahabal): Not ported over the notion of underlying relations, yet. But maybe what I need is
  slightly different anyway, since a mountain cannot be cleanly represented just by a single kind
  of underlying relationship among items.
  """

  def __init__(self, *, items):
    PSObject.__init__(self)
    self.items = items

  def Structure(self):
    return tuple(x.Structure() for x in self.items)
