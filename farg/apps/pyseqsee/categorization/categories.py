"""Defines the categories for objects."""
from farg.apps.pyseqsee.objects import PSElement, PSGroup
from farg.apps.pyseqsee.categorization.logic import InstanceLogic
from farg.core.ltm.storable import LTMNodeContent

class BadCategorySpec(Exception):
  pass

class PyCategory(LTMNodeContent):
  pass

class CategoryAnyObject(PyCategory):
  def IsInstance(self, item):
    return InstanceLogic()

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
    return InstanceLogic()

  def LTMDependentContent(self):
    return set(self.part_categories)

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
      return InstanceLogic(attributes=dict(length=PSElement(magnitude=0)))
    magnitude = item.items[0].magnitude
    if not all(x.magnitude == magnitude for x in item.items):
      return None
    return InstanceLogic(attributes=dict(length=PSElement(magnitude=len(item.items)),
                                         magnitude=PSElement(magnitude=magnitude)))

  def BriefLabel(self):
    return "RepeatedIntegerCategory"


class BasicSuccessorCategory(PyCategory):
  """Category of items such as (2, 3, 4)"""

  def IsInstance(self, item):
    if not isinstance(item, PSGroup):
      return None
    if not all(isinstance(x, PSElement) for x in item.items):
      return None
    if not item.items:
      # So empty. Attribute for magnitude can be anything...
      # TODO(amahabal): Deal with this better.
      return InstanceLogic(attributes=dict(length=PSElement(magnitude=0)))
    start = item.items[0].magnitude
    for offset, elt in enumerate(item.items):
      if elt.magnitude != start + offset:
        return None
    return InstanceLogic(attributes=dict(length=PSElement(magnitude=len(item.items)),
                                         start=PSElement(magnitude=start),
                                         end=PSElement(magnitude=start+len(item.items)-1)))
  def BriefLabel(self):
    return "BasicSuccessorCategory"

class BasicPredecessorCategory(PyCategory):
  """Category of items such as (4, 3, 2)"""

  def IsInstance(self, item):
    if not isinstance(item, PSGroup):
      return None
    if not all(isinstance(x, PSElement) for x in item.items):
      return None
    if not item.items:
      # So empty. Attribute for magnitude can be anything...
      # TODO(amahabal): Deal with this better.
      return InstanceLogic(attributes=dict(length=PSElement(magnitude=0)))
    start = item.items[0].magnitude
    for offset, elt in enumerate(item.items):
      if elt.magnitude != start - offset:
        return None
    return InstanceLogic(attributes=dict(length=PSElement(magnitude=len(item.items)),
                                         start=PSElement(magnitude=start),
                                         end=PSElement(magnitude=start-len(item.items)+1)))

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
      return InstanceLogic(attributes=dict(length=PSElement(magnitude=0)))
    logics = []
    for component in item.items:
      logic = component.DescribeAs(self.base_category)
      if not logic:
        return None
      logics.append(logic)
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
    return InstanceLogic(attributes=dict(length=PSElement(magnitude=len(item.items)),
                                         start=item.items[0],
                                         end=item.items[-1]))

  def BriefLabel(self):
    return "CompoundCategory(%s: %s)" % (self.base_category.BriefLabel(),
                                         ', '.join("%s=%s" % (k, v.BriefLabel())
                                                   for k, v in self.attribute_categories))

  def LTMDependentContent(self):
    out = set(x[1] for x in self.attribute_categories)
    out.add(self.base_category)
    return out
