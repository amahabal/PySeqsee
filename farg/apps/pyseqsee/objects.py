from farg.core.ltm.storable import LTMNodeContent

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
