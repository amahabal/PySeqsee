"""Defines the categories for objects."""
from farg.apps.pyseqsee.objects import PSElement, PSGroup
from farg.apps.pyseqsee.categorization import logic
from farg.apps.pyseqsee.utils import PSObjectFromStructure

PyCategory = logic.PyCategory

class BadCategorySpec(Exception):
  """Raised when the specification for creating a category is somehow wrong.

  Note that this is different from the exception raised when creating instances of categories.
  """
  pass


class CategoryAnyObject(PyCategory):
  def IsInstance(self, item):
    return logic.InstanceLogic()

  def BriefLabel(self):
    return "CategoryAnyObject"

class MultiPartCategory(PyCategory):
  """Category whose instances are made up of N different parts.

  Each part can specify its own category.
  """

  def __init__(self, *, parts_count, part_categories):
    if not isinstance(parts_count, int) or parts_count <= 0:
      raise BadCategorySpec("Strange parts_count")
    if not isinstance(part_categories, tuple) or len(part_categories) != parts_count:
      raise BadCategorySpec("parts_count does not match part_categories")
    if not all(isinstance(x, PyCategory) for x in part_categories):
      print("part cat=", part_categories)
      raise BadCategorySpec("Saw a non-PyCategory as a category for a part")
    self.parts_count = parts_count
    self.part_categories = part_categories

  def BriefLabel(self):
    return "MultiPartCategory(" + ', '.join(x.BriefLabel() for x in self.part_categories) + ")"

  def IsInstance(self, item):
    if not isinstance(item, PSGroup):
      return None
    if not len(item.items) == self.parts_count:
      return None
    for idx, cat in enumerate(self.part_categories):
      if not item.items[idx].DescribeAs(cat):
        return None
    return logic.InstanceLogic()

def CreateRepeatedIntegerFromMagAndLength(magnitude, length):
  return PSObjectFromStructure( (magnitude.magnitude, ) * length.magnitude)

class RepeatedIntegerCategory(PyCategory):
  """Category of items such as (3, 3, 3, 3)."""

  _rules = ('magnitude: NONE', 'length: NONE')
  _object_constructors = {('magnitude', 'length'): CreateRepeatedIntegerFromMagAndLength  }
  _external_vals = dict(PSObjectFromStructure=PSObjectFromStructure)
  _guessers = ('magnitude: instance.items[0]',
               'magnitude: PSObjectFromStructure(1)',
               'length: PSObjectFromStructure(len(instance.items))')

  def BriefLabel(self):
    return "RepeatedIntegerCategory"

  def GetAffordanceForInstance(self, instance):
    return 1  # Fake, replace with something realer...

def CreateSuccessorFromStartAndEnd(start, end):
  return PSObjectFromStructure(tuple(range(start.magnitude, end.magnitude + 1)))

class BasicSuccessorCategory(PyCategory):
  """Category of items such as (2, 3, 4)"""

  _rules = ("end: PSObjectFromStructure(start.magnitude + length.magnitude - 1)",
            "start: PSObjectFromStructure(end.magnitude - length.magnitude + 1)",
            "length: PSObjectFromStructure(end.magnitude - start.magnitude + 1)")
  _external_vals = dict(PSObjectFromStructure=PSObjectFromStructure)
  _object_constructors = {('start', 'end'): CreateSuccessorFromStartAndEnd  }
  _guessers = ('start: instance.items[0]',
               'end: instance.items[-1]',
               # Handles the case where we have an empty list
               'length: PSObjectFromStructure(len(instance.items))',
               'start: PSObjectFromStructure(1)')

  def BriefLabel(self):
    return "BasicSuccessorCategory"

def CreatePredecessorFromStartAndEnd(start, end):
  return PSObjectFromStructure(tuple(range(start.magnitude, end.magnitude - 1, -1)))

class BasicPredecessorCategory(PyCategory):
  """Category of items such as (4, 3, 2)"""

  _rules = ("end: PSObjectFromStructure(start.magnitude - length.magnitude + 1)",
            "start: PSObjectFromStructure(end.magnitude + length.magnitude - 1)",
            "length: PSObjectFromStructure(start.magnitude - end.magnitude + 1)")
  _external_vals = dict(PSObjectFromStructure=PSObjectFromStructure)
  _object_constructors = {('start', 'end'): CreatePredecessorFromStartAndEnd  }
  _guessers = ('start: instance.items[0]',
               'end: instance.items[-1]',
               # Handles the case where we have an empty list
               'length: PSObjectFromStructure(len(instance.items))',
               'start: PSObjectFromStructure(1)')

  def BriefLabel(self):
    return "BasicPredecessorCategory"


class CompoundCategory(PyCategory):
  """Category for things such as ((7), (7, 8), (7, 8, 9)), where components are based on another category."""

  def __init__(self, *, base_category, attribute_categories):
    if not isinstance(base_category, PyCategory):
      raise BadCategorySpec("base_category must be a category")
    if not isinstance(attribute_categories, tuple):
      raise BadCategorySpec("attribute_categories must be a tuple, with each item a (name, cat) pair")
    if not all(isinstance(x, tuple) and len(x) == 2 and isinstance(x[1], PyCategory)
               for x in attribute_categories):
      raise BadCategorySpec("attribute_categories must be a tuple, with each item a (name, cat) pair")
    attributes = tuple(x[0] for x in attribute_categories)
    if attributes != tuple(sorted(attributes)):
      raise BadCategorySpec("Attributes must be sorted")
    self.base_category = base_category
    self.attribute_categories = attribute_categories
    self._attribues = attributes

  def IsInstance(self, item):
    if not isinstance(item, PSGroup):
      return None
    if not item.items:
      # So empty. Attribute for magnitude can be anything...
      # TODO(amahabal): Deal with this better.
      return logic.InstanceLogic(attributes=dict(length=PSElement(magnitude=0)))
    logics = []
    for component in item.items:
      inst_logic = component.DescribeAs(self.base_category)
      if not inst_logic:
        return None
      logics.append(inst_logic)
    for attr, attr_cat in self.attribute_categories:
      values_for_attr = tuple(x.GetAttributeOrNone(attribute=attr) for x in logics)
      if not all(values_for_attr):
        return None
      attr_gp = PSGroup(items=values_for_attr)
      attr_logic = attr_gp.DescribeAs(attr_cat)
      if not attr_logic:
        return None
      # TODO: also store the attr logic somewhere; should be accessible from the logic of the bigger
      # group.
    return logic.InstanceLogic(attributes=dict(length=PSElement(magnitude=len(item.items)),
                                               start=item.items[0],
                                               end=item.items[-1]))

  def BriefLabel(self):
    return "CompoundCategory(%s: %s)" % (self.base_category.BriefLabel(),
                                         ', '.join("%s=%s" % (k, v.BriefLabel())
                                                   for k, v in self.attribute_categories))
