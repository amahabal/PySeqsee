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

"""Classes to deal with categories and their instances, including the base class for
categories.

An example will help describe all that happens here. We will use the category 'Ascending'
from Seqsee. Instances of this category are objects such as '(1 2 3)' and '(7 8 9 10)'.
Objects need to have CategorizableMixin in their class hierarchy: it provides methods to
store the discovered categories and their bindings.

A category is a class (deriving from Category).

Adding a category to an instance::

  bindings = item.DescribeAs(category)

The following also returns a binding, but does not store the membership information::

  bindings = category.IsInstance(item)

"""

from farg.core.exceptions import FargError
from farg.core.meta import MemoizedConstructor
from farg.core.ltm.storable import LTMStorableMixin

class Category(LTMStorableMixin, metaclass=MemoizedConstructor):
  """The base class of any category in the FARG system.
  
  Any derivative class must define the following class methods:
  
  * IsInstance (which would return a binding),
  * FindMapping (given two categorizables, returns a mapping between the two)
  * ApplyMapping (given a mapping and a categorizable, returns a new item). 
  """

  def IsInstance(self, object):
    """Is object an instance of this category?
    
    If it is not, `None` is returned. If it is, a binding object is returned.
    """
    raise FargError("IsInstance makes no sense on base category.")

