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

"""Seqsee-specific categories.

These will include (not all implemented yet):

* Numeric Categories:

  * Number
  * Prime
  * Even and Odd
  
* Structural Categories:

  * Ascending
  * Descending
  * Mountain
  * Size2, Size3, etc.
  
* Mapping Based Categories:

  * Given a mapping, a category can be defined whose elements are such that successive 
    elements are associated by this mapping.

Numeric Categories
--------------------

Members may only be SElements, and membership depends only on the magnitude of the SElement. 
These derive from NumericCategory, and must define the class method NumericIsInstance.

Structural Categories
-----------------------

Members are SObjects (may be groups or elements), and membership depends only on the 
structure. These derive from StructuralCategory, and must define class method 
StructuralIsInstance.

Parametrized Categories
-------------------------

This is a category "factory": subclasses of ParametrizedCategory must define a classmethod
Construct that returns a category (i.e., a subclass of Category).

If FooCategory is a subclass of ParametrizedCategory, we could say::

  cat1 = FooCategory.Create(x=3)
  # cat1 is subclass of Category.
  cat2 = FooCategory.Create(x=3)  # Returns the same cached class.

"""

from farg.apps.seqsee.mapping import NumericMapping, StructuralMapping
from farg.apps.seqsee.sobject import SElement, SObject
from farg.apps.seqsee.structure_utils import StructureDepth
from farg.core.categorization.binding import Binding
from farg.core.categorization.category import Category
from farg.core.exceptions import FargError, FargException

class SeqseeObjectCategory(Category):
  """Base for categories whose instances are groups in Seqsee.

     Any derivative class must define the following class methods:

     * FindMapping (given two categorizables, returns a mapping between the two)
     * ApplyMapping (given a mapping and a categorizable, returns a new item). 
  """
  def FindMapping(self, categorizable1, categorizable2):
    """Finds a mapping between two objects based on a particular category."""
    raise FargError("IsInstance makes no sense on base category.")

  def ApplyMapping(self, categorizable, mapping):
    """Apply a mapping to a categorizable to obtain a different categorizable."""
    raise FargError("IsInstance makes no sense on base category.")


class NumericCategory(SeqseeObjectCategory):
  """Base class for categories whose instances are SElements, and membership depends only on 
     the magnitude.
  """

  def IsInstance(self, item):
    if not isinstance(item, SElement):
      return None
    magnitude = item.magnitude
    return self.NumericIsInstance(magnitude)

class StructuralCategory(SeqseeObjectCategory):
  """Base class whose membership depends on the structure (e.g., ascending, mountain)."""

  def IsInstance(self, item):
    return self.StructuralIsInstance(item.Structure())


  def GetMapping(self, item1, item2):
    binding1 = item1.DescribeAs(self)
    if not binding1: return None
    binding2 = item2.DescribeAs(self)
    if not binding2: return None
    return self.GetMappingBetweenBindings(binding1, binding2)


  def GetMappingBetweenBindings(self, binding1, binding2):
    """Get mapping between a pair of bindings. This should eventually be replaced by a space
       (as discussed in the last chapter of the dissertation). For now, I have a simple
       mechanism.
    """
    bindings_mapping = {}
    for k, v in binding1.bindings.items():
      if k in binding2.bindings:
        v2 = binding2.bindings[k]
        possible_mapping = GetNaiveMapping(v, v2)
        if possible_mapping:
          bindings_mapping[k] = possible_mapping
    if self.AreAttributesSufficientToBuild(list(bindings_mapping.keys())):
      return StructuralMapping(category=self,
                               bindings_mapping=frozenset(list(bindings_mapping.items())))
    return None

class Number(NumericCategory):

  def BriefLabel(self):
    return 'Number'

  def NumericIsInstance(self, val):
    return Binding()


  def GetMapping(self, item1, item2):
    index1, index2 = item1.magnitude, item2.magnitude
    diff_string = NumericMapping.DifferenceString(index1, index2)
    if diff_string:
      return NumericMapping(diff_string, Number())
    else:
      return None


  def ApplyMapping(self, mapping, item):
    name = mapping.name
    if name == 'same':
      return item.DeepCopy()
    if name == 'pred':
      return SObject.Create(item.magnitude - 1)
    if name == 'succ':
      return SObject.Create(item.magnitude + 1)

class PrecomputedNumberList(NumericCategory):
  """Categories such as Prime and Fibonacci which are provided as a pre-computed list."""

  #: Must be provided with a number list.
  number_list = None

  #: A brief label must be provided.
  brief_label = None

  def __init__(self):
    NumericCategory.__init__(self)

    # These are stored on the class (where they belong).
    self.__class__.smallest_known_element = min(self.number_list)
    self.__class__.largest_known_element = max(self.number_list)

  def BriefLabel(self):
    return self.brief_label

  def NumericIsInstance(self, val):
    try:
      index = self.number_list.index(val)
      return Binding(index=index)
    except ValueError:
      return None

  def _NextNumber(self, val):
    if val >= self.largest_known_element:
      return None
    return self.number_list[self.number_list.index(val) + 1]

  def _PrevNumber(self, val):
    if val <= self.smallest_known_element:
      return None
    return self.number_list[self.number_list.index(val) - 1]

  def GetMapping(self, item1, item2):
    binding1 = item1.DescribeAs(self)
    if not binding1: return None
    binding2 = item2.DescribeAs(self)
    if not binding2: return None

    index1, index2 = (binding1.GetBindingsForAttribute('index'),
                      binding2.GetBindingsForAttribute('index'))
    diff_string = NumericMapping.DifferenceString(index1, index2)
    if diff_string:
      return NumericMapping(diff_string, self)
    else:
      return None


  def ApplyMapping(self, mapping, item):
    name = mapping.name
    if name == 'same':
      return item.DeepCopy()
    if name == 'pred':
      val = self._PrevNumber(item.magnitude)
      if val:
        return SObject.Create(val)
      else:
        return None
    if name == 'succ':
      val = self._NextNumber(item.magnitude)
      if val:
        return SObject.Create(val)
      else:
        return None

class Prime(PrecomputedNumberList):
  brief_label = 'Prime'
  number_list = [
      int(x) for x in
      '2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97'.split()]

class Squares(PrecomputedNumberList):
  brief_label = 'Square'
  number_list = [x * x for x in range(1, 100)]

class TriangularNumbers(PrecomputedNumberList):
  brief_label = 'TriangularNumber'
  number_list = [ x * (x + 1) / 2 for x in range(1, 100)]

class Ascending(StructuralCategory):

  def BriefLabel(self):
    return 'Ascending'


  def StructuralIsInstance(self, structure):
    depth = StructureDepth(structure)
    if depth >= 2: return None
    if depth == 0:
      return Binding(start=structure, end=structure, length=1)
    # So depth = 1
    for idx, v in enumerate(structure[1:], 1):
      if v != structure[idx - 1] + 1:
        return None
    return Binding(start=SObject.Create(structure[0]),
                   end=SObject.Create(structure[-1]),
                   length=SObject.Create(structure[-1] - structure[0] + 1))


  def Create(self, bindings):
    start = bindings.get('start', None)
    end = bindings.get('end', None)
    length = bindings.get('length', None)
    if not start:
      if not end or not length:
        raise FargError("Create called when attributes insufficient to build.")
      start_mag = end.magnitude - length.magnitude + 1
      return SObject.Create(list(range(start_mag, end.magnitude + 1)))
    if not end:
      if not start or not length:
        raise FargError("Create called when attributes insufficient to build.")
      end_mag = start.magnitude + length.magnitude - 1
      return SObject.Create(list(range(start.magnitude, end_mag + 1)))
    return SObject.Create(list(range(start.magnitude, end.magnitude + 1)))


  def AreAttributesSufficientToBuild(self, attributes):
    return len(set(attributes).intersection(set(['start', 'end', 'length']))) >= 2

def GetNaiveMapping(v1, v2):
  if isinstance(v1, int) and isinstance(v2, int):
    diff_string = NumericMapping.DifferenceString(v1, v2)
    if diff_string:
      return NumericMapping(name=diff_string, category=Number())
    else:
      return None
  common_categories = v1.GetCommonCategoriesSet(v2)
  if common_categories:
    # ... ToDo: Don't merely use the first category!
    cat = list(common_categories)[0]
    return cat.GetMapping(v1, v2)
  if isinstance(v1, SElement) and isinstance(v2, SElement):
    return GetNaiveMapping(v1.magnitude, v2.magnitude)
  return None


class SizeNCategory(StructuralCategory):

  def __init__(self, size):
    if size == 1:
      raise FargError("Attempt to create a SizeN category with size=1")
    self.size = size

  def BriefLabel(self):
    return 'SizeN(%d)' % self.size

  def StructuralIsInstance(self, structure):
    if isinstance(structure, int):
      return None
    if len(structure) != self.size:
      return None
    bindings = {}
    for idx, item in enumerate(structure, 1):
      bindings['pos_%d' % idx] = SObject.Create(item)
    return Binding(**bindings)


  def AreAttributesSufficientToBuild(self, attributes):
    for idx in range(1, self.size + 1):
      if 'pos_%d' % idx not in attributes:
        return False
    return True


  def Create(self, bindings):
    structure = [bindings['pos_%d' % x] for x in range(1, self.size + 1)]
    return SObject.Create(structure)

class MappingBasedCategory(StructuralCategory):
  def __init__(self, mapping):
    self.mapping = mapping

  def BriefLabel(self):
    return 'MBC(%s)' % self.mapping.BriefLabel()

  def IsInstance(self, item):
    if isinstance(item, SElement):
      # Probably the wrong thing to do.
      return None
    for item_part in item.items:
      if not item_part.DescribeAs(self.mapping.category):
        return self.IsDegenerateInstance(item)
    # So all items can be described as members of category...
    for idx, itempart in enumerate(item.items[1:], 1):
      if not self.mapping.IsPairConsistent(item.items[idx - 1], itempart):
        return self.IsDegenerateInstance(item)
    # Okay, so valid.
    return Binding(start=item.items[0], length=SObject.Create(len(item.items)))


  def IsDegenerateInstance(self, item):
    if not item.DescribeAs(self.mapping.category):
      return None
    return Binding(start=item, length=SObject.Create(1))


  def AreAttributesSufficientToBuild(self, attributes):
    return 'start' in attributes and 'length' in attributes


  def Create(self, bindings):
    items = [SObject.Create(bindings['start'])]
    for _i in range(1, bindings['length'].magnitude):
      if not items[-1].DescribeAs(self.mapping.category):
        raise FargException("Unable to create object")
      next_item = self.mapping.Apply(items[-1])
      if not next_item:
        raise FargException("Unable to create object")
      items.append(next_item)
    return SObject.Create(items)
