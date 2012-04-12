# Copyright (C) 2011, 2012  Abhijit Mahabal

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

stopping_conditions_dict = dict()

def RegisterStoppingCondition(*, condition_name):
  def decorator(func):
    stopping_conditions_dict[condition_name] = func
    return func
  return decorator

@RegisterStoppingCondition(condition_name="group_present")
def CheckGroupPresence(controller):
  return bool(controller.workspace.groups)
