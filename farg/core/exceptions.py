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

  def __init__(self, msg=''):
    Exception.__init__(self)
    #: Message to be displayed.
    self.msg = msg
    self.stack_trace = list(takewhile((lambda x: x.find('FargError.__init__') == -1),
                                      traceback.format_stack(limit=8)))
    print("FargError: %s:%s" % (msg, self.stack_trace))

  def __str__(self):
    return "FargError:" + self.msg + str(self.stack_trace)


class FargException(Exception):
  """Base class for FARG-specific exceptions."""
  pass

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
