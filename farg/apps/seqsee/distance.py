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
"""Code for keeping track of distances between items in the workspace.

Distance can be in either of two units: numbers or groups. That is, the distance between
1 and 2 in "1 (7 8) 2" is either 2 numbers or 1 group. Adjacent elements have distance 0
in either units.
"""
from farg.core.ltm.storable import LTMStorableMixin
from farg.core.meta import MemoizedConstructor
class Distance(LTMStorableMixin):
  def __init__(self, *, value, unit):
    self.value = value
    self.unit = unit

  def UnitIsElements(self):
    return self.unit == "Elements"

  def UnitIsGroups(self):
    return self.unit == "Groups"

class DistanceInElements(Distance, metaclass=MemoizedConstructor):
  def __init__(self, *, value, unit="Elements"):
    assert value >= 0 and unit == "Elements"
    Distance.__init__(self, value=value, unit="Elements")

  def BriefLabel(self):
    if self.value == 1:
      return "Distance: 1 element"
    else:
      return "Distance: %d elements" % self.value

class DistanceInGroups(Distance, metaclass=MemoizedConstructor):
  def __init__(self, *, value, unit="Groups"):
    assert value >= 0 and unit == "Groups"
    Distance.__init__(self, value=value, unit="Groups")

  def BriefLabel(self):
    if self.value == 1:
      return "Distance: 1 group"
    else:
      return "Distance: %d groups" % self.value
