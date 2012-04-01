from farg.exceptions import AnswerFoundException, NoAnswerException

class MemoizedConstructor(type):
  def __init__(self, name, bases, class_dict):
    super(MemoizedConstructor, self).__init__(name, bases, class_dict)
    self.__memo__ = dict()

  def __call__(self, *args, **kw):
    memo_key = (tuple(args), frozenset(list(kw.items())))
    if memo_key not in self.__memo__:
      self.__memo__[memo_key] = super(MemoizedConstructor, self).__call__(*args, **kw)
    return self.__memo__[memo_key]


class SubspaceMeta(type):
  def __call__(self, parent_controller, nsteps=4, workspace_arguments=dict()):
    try:
      self.QuickReconn(parent_controller=parent_controller, **workspace_arguments)
    except NoAnswerException:
      return None
    except AnswerFoundException as e:
      return e.answer

    # Okay, so a QuickReconn recommends a deeper exploration.
    instance = super(SubspaceMeta, self).__call__(parent_controller, nsteps,
                                                  workspace_arguments)
    try:
      instance.Run()
    except AnswerFoundException as e:
      return e.answer
    except NoAnswerException:
      return None
    return None
