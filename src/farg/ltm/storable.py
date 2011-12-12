class LTMStorableMixin(object):
  """Any class whose instances should be stored in LTM must adhere to certain semantics,
  and subclass from this class.
  
  For a given set of arguments, this class ensures that only a single object is created.
  """
  memos = {}

  @classmethod
  def Create(cls, **kwargs):
    key = frozenset(kwargs.items())
    if key not in cls.memos:
      new_instance = cls(**kwargs)
      cls.memos[key] = new_instance
      return new_instance
    return cls.memos[key]

  @classmethod
  def ClearMemos(cls):
    memos = {}

  def BriefLabel(self):
    """A brief label useful for, for instance, display in LTM viewer."""
    return '%s: ???' % self.__class__.__name__

class LTMMadeStorable(object):
  def __init__(self, cls, storable):
    self.cls = cls
    self.storable = storable

  memos_ltm_madestorable = {}

  @staticmethod
  def Create(cls, storable):
    key = (cls, storable)
    if key not in LTMMadeStorable.memos_ltm_madestorable:
      new_instance = LTMMadeStorable(cls, storable)
      LTMMadeStorable.memos_ltm_madestorable[key] = new_instance
      return new_instance
    return LTMMadeStorable.memos_ltm_madestorable[key]

class LTMMakeStorableMixin(object):
  """Some classes may not be storable in an LTM, but they may define a way to obtain unique LTM
  nodes corresponding to them. An example is SObject: each time an SObject is created, it must 
  produce a different object, but they should map to the same LTM node.
  
  Such classes may use this mixin and add a GetStorable method instead."""

  @classmethod
  def CreateLTMStorable(cls, item):
    return LTMMadeStorable.Create(cls, item.GetStorable())

