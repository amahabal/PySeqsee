class FargError(Exception):
  """Base class for untrappable errors (indicating bugs)."""
  pass

class FargException(Exception):
  """Base class for FARG-specific exceptions."""
  pass

class ConflictingGroupException(FargException):
  """If an attempt is made to add a group to the workspace that conflicts some existing group(s),
  this exception is raised."""
  def __init__(self, conflicting_groups):
    #: The groups that conflict.
    self.conflicting_groups = conflicting_groups

class YesNoException(FargException):
  """An exception that requests the UI to ask a yes/no question.
  
  When the user answers, a callback is made to the controller with this info.
  """

  def __init__(self, question_string, callback):
    self.question_string = question_string
    self.callback = callback
