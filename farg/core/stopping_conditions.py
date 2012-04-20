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

"""Manage stopping conditions."""

class StoppingConditionNotFound(Exception):
  def __init__(self, name):
    self.name = name

  def __str__(self):
    return 'No stopping condition registered for %s' % self.name


class StoppingConditions:
  """Manage the set of stopping conditions."""

  #: The known set of stopping conditions.
  conditions = dict()

  @classmethod
  def RegisterStoppingCondition(self, condition_name, condition_fn):
    """Remember a new stopping condition."""
    self.conditions[condition_name] = condition_fn

  @classmethod
  def GetStoppingCondition(self, condition_name):
    """Returns a stopping condition function. Raises an exception if none found."""
    if condition_name in self.conditions:
      return self.conditions[condition_name]
    else:
      raise StoppingConditionNotFound(condition_name)

  @classmethod
  def StoppingConditionsList(self):
    """Returns list of known stopping conditions."""
    return list(self.conditions.keys())

def RegisterStoppingCondition(stopping_conditions_class, *, condition_name):
  def decorator(func):
    stopping_conditions_class.RegisterStoppingCondition(condition_name, func)
    return func
  return decorator

