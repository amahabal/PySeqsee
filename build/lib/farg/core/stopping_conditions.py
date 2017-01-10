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

"""Manage stopping conditions.

For debugging or testing reasons, one may want to run an application until a particular
condition is met. This module manages stopping conditions.
"""


class StoppingConditionNotFound(Exception):
  """Raised when requested stopping condition has not been registered."""

  def __init__(self, name):
    Exception.__init__(self)
    #: Name of condition.
    self.name = name

  def __str__(self):
    return 'No stopping condition registered for %s' % self.name


class StoppingConditions:  # No __init__. pylint:disable=W0232
  """Manage the set of stopping conditions."""

  #: The known set of stopping conditions.
  conditions = dict()  # Not a constant. pylint: disable=C6409

  @classmethod
  def RegisterStoppingCondition(cls, condition_name, condition_fn):
    """Remember a new stopping condition.

    Args:
      condition_name: Name of the stopping condition.
      condition_fn: A function that gets the controller as its only argument.
    """
    cls.conditions[condition_name] = condition_fn

  @classmethod
  def GetStoppingCondition(cls, condition_name):
    """Returns a stopping condition function given name.

    Args:
      condition_name: Name of stopping condition.

    Returns:
      A function taking a single argument (a controller).

    Raises:
      StoppingConditionNotFound: if name not found.
    """
    if condition_name in cls.conditions:
      return cls.conditions[condition_name]
    else:
      raise StoppingConditionNotFound(condition_name)

  @classmethod
  def StoppingConditionsList(cls):
    """Returns list of known stopping conditions."""
    return list(cls.conditions.keys())


def RegisterStoppingCondition(stopping_conditions_class, *, condition_name):
  """Decorator for registering a stopping condition on a class.

  Args:
    stopping_conditions_class: The class for which stopping condition is being defined.

  Keyword-only Args:
    condition_name: Name of the stopping condition.

  Returns:
    A decorated function identical to input. Decoration useful only for its side-effect.

  Usage::

    @RegisterStoppingCondition(SomeSubclassOfStoppingConditions, condition_name='foo')
    def CheckFoo(controller):
      ... do something ...
  """

  def Decorator(func):
    """Return input after registering it."""
    stopping_conditions_class.RegisterStoppingCondition(condition_name, func)
    return func
  return Decorator
