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
from farg.core.meta import MemoizedConstructor

class LTMNodeContent(object, metaclass=MemoizedConstructor):
  """Base class for things that can be the actual contents of nodes.

  This class has to satisfy extra constraints since it needs to be vivifiable: that is, we need the
  ability to dump this out into a file, and in a later run, construct an object from it again.

  To achieve this, the __dict__ of this object is pickled, and in the later run, unpickled and
  passed to the constructor.
  """

  def BriefLabel(self):
    raise Exception("BriefLabel should have been implemented by subclass %s" % self.__class__)

  def LTMDependentContent(self):
    """Returns nodes whose existence is necessary for fully defining this node."""
    return ()

  def GetLTMStorableContent(self):
    return self

class LTMStorableMixin(object):
  """Base class for items that may be stored in the long-term memory.

  Any class whose instances should be stored in LTM must adhere to certain semantics,
  and subclass from this class. Typically, it would also use MemoizedConstructor as a
  metaclass.
  """
  def GetLTMStorableContent(self):
    return self

  def BriefLabel(self):
    raise Exception("BriefLabel should have been implemented by subclass %s" % self.__class__)

  def LTMDependentContent(self):
    """Returns nodes whose existence is necessary for fully defining this node."""
    return ()
