class Mapping(object):
  def __init__(self):
    raise Exception("Cannot create an instance of a category.")

  @classmethod
  def Apply(cls, *entities):
    if len(entities) != cls.arity:
      raise Exception("Wrong arity")
    for entity in entities:
      if not isinstance(entity, cls.realm):
        raise Exception("Wrong type of entity.")
    return cls.fn(*entities)
  
  @classmethod
  def Inverse(cls):
    if hasattr(cls, '_stored_inverse'):
      return cls._stored_inverse
    class inv(Mapping):
      realm = cls.realm
      arity = cls.arity
      fn = staticmethod(cls.rev_fn)
      rev_fn = staticmethod(cls.fn)
    cls._stored_inverse = inv
    inv._stored_inverse = cls
    return inv
    