class Category:
  def __init__(self):
    raise Exception("Cannot create an instance of a category.")
  
  @classmethod
  def CheckIfInstance(cls, entity):
    bindings = cls.IsInstance(entity)
    if not bindings:
      return False
    else:
      cm = entity.cm
      for k, v in bindings.iteritems():
        if k in cls.global_attributes:
          cm.AddAttribute(k, v)
        else:
          cm.AddAttribute(k, v, cls)