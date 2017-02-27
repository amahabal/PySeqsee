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
"""Seqsee-specific exceptions."""
from farg.core.exceptions import FargException
class SeqseeException(FargException):
  """Base class of all Seqsee exceptions."""
  pass

class ConflictingGroupException(SeqseeException):
  """If an attempt is made to add a group to the workspace that conflicts some existing
     group(s), this exception is raised.
  """
  def __init__(self, conflicting_groups):
    #: The groups that conflict.
    FargException.__init__(self)
    self.conflicting_groups = conflicting_groups

  def __str__(self):
    return "ConflictingGroupException(conflicting_groups=%s)" % str(self.conflicting_groups)


class CannotReplaceSubgroupException(SeqseeException):
  """Attempt to replace a group that is a subgroup."""
  def __init__(self, supergroups):
    FargException.__init__(self)
    self.supergroups = supergroups

  def __str__(self):
    return "CannotReplaceSubgroupException(supergroups=%s)" % str(self.supergroups)
