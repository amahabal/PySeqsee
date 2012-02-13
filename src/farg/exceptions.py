import traceback
from itertools import takewhile

class FargError(Exception):
  """Base class for untrappable errors (indicating bugs)."""
  pass

class FargException(Exception):
  """Base class for FARG-specific exceptions."""
  def __init__(self):
    self.stack_trace = list(takewhile((lambda x: x.find('FargException.__init__') == -1),
                                      traceback.format_stack(limit=5)))

class AnswerFoundException(FargException):
  """Raised by a subspace when it believes that an answer has been found."""
  def __init__(self, answer):
    FargException.__init__(self)
    self.answer = answer

class NoAnswerException(FargException):
  """Raised by a subspace when it is realized that no answer is forthcoming."""
  def __init__(self):
    FargException.__init__(self)

class ConflictingGroupException(FargException):
  """If an attempt is made to add a group to the workspace that conflicts some existing
     group(s), this exception is raised.
  """
  def __init__(self, conflicting_groups):
    #: The groups that conflict.
    FargException.__init__(self)
    self.conflicting_groups = conflicting_groups

  def __str__(self):
    return "ConflictingGroupException(conflicting_groups=%s)" % str(self.conflicting_groups)

class CannotReplaceSubgroupException(FargException):
  """Attempt to replace a group that is a subgroup."""
  def __init__(self):
    FargException.__init__(self)

class YesNoException(FargException):
  """An exception that requests the UI to ask a yes/no question.
  
  When the user answers, a callback is made to the controller with this info.
  """

  def __init__(self, question_string, callback):
    FargException.__init__(self)
    self.question_string = question_string
    self.callback = callback
