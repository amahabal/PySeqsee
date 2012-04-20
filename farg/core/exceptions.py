# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

import traceback
from itertools import takewhile

class FargError(Exception):
  """Base class for untrappable errors (indicating bugs)."""
  def __init__(self, msg):
    self.stack_trace = list(takewhile((lambda x: x.find('FargError.__init__') == -1),
                                      traceback.format_stack(limit=8)))
    print('FargError: ', msg)

class FargException(Exception):
  """Base class for FARG-specific exceptions."""
  def __init__(self):
    self.stack_trace = list(takewhile((lambda x: x.find('FargException.__init__') == -1),
                                      traceback.format_stack(limit=8)))

class BatchModeStopException(Exception):
  """Base class of ways of stopping during batch mode."""
  def __init__(self, *, codelet_count):
    Exception.__init__(self)
    self.codelet_count = codelet_count

class StoppingConditionMet(BatchModeStopException):
  def __str__(self):
    return 'StoppingConditionMet after %d codelets' % self.codelet_count

class SuccessfulCompletion(BatchModeStopException):
  pass

class AnswerFoundException(BatchModeStopException):
  """Raised by a subspace when it believes that an answer has been found."""
  def __init__(self, answer, *, codelet_count):
    BatchModeStopException.__init__(self, codelet_count=codelet_count)
    self.answer = answer

class NoAnswerException(BatchModeStopException):
  """Raised by a subspace when it is realized that no answer is forthcoming."""
  def __init__(self, *, codelet_count):
    BatchModeStopException.__init__(self, codelet_count=codelet_count)

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
  def __init__(self, supergroups):
    FargException.__init__(self)
    self.supergroups = supergroups

  def __str__(self):
    return "CannotReplaceSubgroupException(supergroups=%s)" % str(self.supergroups)


class YesNoException(FargException):
  """An exception that requests the UI to ask a yes/no question.
  
  When the user answers, a callback is made to the controller with this info.
  """

  def __init__(self, question_string, callback):
    FargException.__init__(self)
    self.question_string = question_string
    self.callback = callback
