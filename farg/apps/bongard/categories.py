# This file defines categories used by Bongard.

import math

from farg.core.categorization.category import Category
from farg.core.categorization.binding import Binding
from farg.core.exceptions import FargError

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

class XModN(Category):
  """Category whose instances leave a remainder of X when divided by N.

  X should be a number between 0 and N-1, inclusive.
  """

  def __init__(self, x, n):
    self.x = x
    self.n = n
    if n == 0:
      raise FargError("Modulo 0 makes no sense")
    if x < 0 or x >= n:
      raise FargError("x must be between 0 and %d:  %d mod %d not supported" % (n - 1, x, n))

  def BriefLabel(self):
    return "%d mod %d" % (self.x, self.n)
  
  def IsInstance(self, entity):
    magnitude = entity.magnitude
    remainder = magnitude % self.n
    if remainder == self.x:
      return Binding(k=(magnitude - self.x) / self.n)
    return None
