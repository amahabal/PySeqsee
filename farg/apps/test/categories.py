# This file defines categories used by Test.

import math

from farg.core.categorization.category import Category
from farg.core.categorization.binding import Binding

class TestCategory(Category):
  """Base class for categories in the Test application."""

  def __str__(self):
    return self.brief_label
