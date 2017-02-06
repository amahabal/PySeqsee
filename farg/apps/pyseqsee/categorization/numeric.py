from farg.apps.pyseqsee.categorization.categories import PyCategory
from farg.apps.pyseqsee.categorization.logic import InstanceLogic
from farg.apps.pyseqsee.objects import PSElement

class NumericCategory(PyCategory):
  """Abstract base class for categories of integers."""

  def IsInstance(self, item):
    if not isinstance(item, PSElement):
      return None
    return self.IsNumericInstance(magnitude=item.magnitude)

class CategoryEvenInteger(NumericCategory):
  def IsNumericInstance(self, *, magnitude):
    if magnitude % 2 != 0:
      return None
    return InstanceLogic()

class PrecomputedNumberList(NumericCategory):
  """Category based on a provided list of numbers."""
  number_list = None

  def IsNumericInstance(self, *, magnitude):
    try:
      index = self.number_list.index(magnitude)
      return InstanceLogic(attributes=dict(index=PSElement(magnitude=index)))
    except ValueError:
      return None

class CategoryPrime(PrecomputedNumberList):
  number_list = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
                 83, 89, 97)
