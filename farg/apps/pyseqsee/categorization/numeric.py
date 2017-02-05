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
