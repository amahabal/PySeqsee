class LTMStorableMixin(object):
  """Any class whose instances should be stored in LTM must adhere to certain semantics,
  and subclass from this class. Typically, it would also use MemoizedConstructor as a
  metaclass.
  
  For a given set of arguments, this class ensures that only a single object is created.
  """
  def GetLTMStorableContent(self):
    return self

  def LTMDisplayLabel(self):
    return self.BriefLabel()

  def BriefLabel(self):
    raise Exception("BriefLabel should have been imported by subclass %s" % self.__class__)

  def LTMDependentContent(self):
    """Returns nodes whose existence is necessary for fully defining this node."""
    return ()
