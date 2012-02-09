class MemoizedConstructor(type):
  def __init__(self, name, bases, class_dict):
    super(MemoizedConstructor, self).__init__(name, bases, class_dict)
    self.__memo__ = dict()

  def __call__(self, *args, **kw):
    memo_key = (tuple(args), frozenset(kw.items()))
    if memo_key not in self.__memo__:
      self.__memo__[memo_key] = super(MemoizedConstructor, self).__call__(*args, **kw)
    return self.__memo__[memo_key]
