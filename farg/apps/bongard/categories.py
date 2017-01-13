# This file defines categories used by Bongard.

import math

from farg.core.categorization.category import Category
from farg.core.categorization.binding import Binding

class Square(Category):
  """Category whose instances are IntegerObject that are square numbers."""

  def BriefLabel(self):
    return "Square"

  def IsInstance(self, entity):
    magnitude = entity.magnitude
    if magnitude < 0:
      return None  # Not an instance.
    root = math.sqrt(magnitude)
    if root != int(root):
      return None
    return Binding(sqroot=root)
