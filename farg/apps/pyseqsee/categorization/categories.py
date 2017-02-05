"""Defines the categories for objects."""
from farg.core.meta import MemoizedConstructor
from farg.apps.pyseqsee.objects import PSElement, PSGroup
from farg.apps.pyseqsee.categorization.logic import InstanceLogic

class BadCategorySpec(Exception):
  pass

class PyCategory(metaclass=MemoizedConstructor):
  pass

class CategoryAnyObject(PyCategory):
  def IsInstance(self, item):
    return InstanceLogic

class MultiPartCategory(PyCategory):
  """Category whose instances are made up of N different parts.

  Each part can specify its own category.
  """

  def __init__(self, *, parts_count, part_categories):
    if not isinstance(parts_count, int) or parts_count <= 0:
      raise BadCategorySpec()
    if not isinstance(part_categories, tuple) or len(part_categories) != parts_count:
      raise BadCategorySpec()
    if not all(isinstance(x, PyCategory) for x in part_categories):
      raise BadCategorySpec()
    self.parts_count = parts_count
    self.part_categories = part_categories

  def IsInstance(self, item):
    if not isinstance(item, PSGroup):
      return None
    if not len(item.items) == self.parts_count:
      return None
    for idx, cat in enumerate(self.part_categories):
      if not item.items[idx].DescribeAs(cat):
        return None
    return InstanceLogic()

class RepeatedIntegerCategory(PyCategory):
  """Category of items such as (3, 3, 3, 3)."""

  def IsInstance(self, item):
    if not isinstance(item, PSGroup):
      return None
    if not all(isinstance(x, PSElement) for x in item.items):
      return None
    if not item.items:
      # So empty. Attribute for magnitude can be anything...
      # TODO(amahabal): Deal with this better.
      return InstanceLogic(attributes=dict(length=0))
    magnitude = item.items[0].magnitude
    if not all(x.magnitude == magnitude for x in item.items):
      return None
    return InstanceLogic(attributes=dict(length=len(item.items),
                                         magnitude=magnitude))
