# This file defines categories used by Bongard.

import math

from farg.core.categorization.category import Category
from farg.core.categorization.binding import Binding

class BongardCategory(Category):
  """Base class for categories in the Bongard application."""

  def __str__(self):
    return self.brief_label
