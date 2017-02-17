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
  _rules = ('it: NONE', )
  _guessers = ('it: instance', )

  def __init__(self):
    self._object_constructors = {('it',): self.CreateFromIt  }
    PyCategory.__init__(self)

  def CreateFromIt(self, it):
    return it

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
      raise BadCategorySpec("Saw a non-PyCategory as a category for a part")
    self.parts_count = parts_count
    self.part_categories = part_categories

    rules = []
    self._external_vals = dict(PSGroup=PSGroup, Verify=logic.Verify)
    for x in range(parts_count):
      var = 'part_%d' % (x + 1)
      cat_name = 'cat_%d' % (x + 1)
      rule = '%s: Verify(%s, %s.DescribeAs(%s))' % (var, var, var, cat_name)
      rules.append(rule)
      self._external_vals[cat_name] = part_categories[x]
    self._rules = tuple(rules)
    self._guessers = tuple('part_%d: instance.items[%d]' % (x+1, x) for x in range(parts_count))
 
    def CreateGivenParts(**parts_def):
      parts = []
      for x in range(parts_count):
        parts.append(parts_def['part_%d' % (x + 1)])
      return PSGroup(items=parts)

    self._object_constructors = {tuple('part_%d' % (x + 1) for x in range(parts_count)): CreateGivenParts}
    PyCategory.__init__(self)

  def BriefLabel(self):
    return "MultiPartCategory(" + ', '.join(x.BriefLabel() for x in self.part_categories) + ")"

class RepeatedIntegerCategory(PyCategory):
  """Category of items such as (3, 3, 3, 3)."""

  _rules = ('magnitude: NONE', 'length: NONE')
  _external_vals = dict(PSObjectFromStructure=PSObjectFromStructure)
  _guessers = ('magnitude: instance.items[0]',
               'magnitude: PSObjectFromStructure(1)',
               'length: PSObjectFromStructure(len(instance.items))')

  def __init__(self):
    self._object_constructors = {('magnitude', 'length'): self.CreateFromMagAndLength  }
    PyCategory.__init__(self)

  def CreateFromMagAndLength(self, magnitude, length):
    return PSObjectFromStructure( (magnitude.magnitude, ) * length.magnitude)

  def BriefLabel(self):
    return "RepeatedIntegerCategory"

  def GetAffordanceForInstance(self, instance):
    return 1  # Fake, replace with something realer...

class BasicSuccessorCategory(PyCategory):
  """Category of items such as (2, 3, 4)"""

  _rules = ("end: PSObjectFromStructure(start.magnitude + length.magnitude - 1)",
            "start: PSObjectFromStructure(end.magnitude - length.magnitude + 1)",
            "length: PSObjectFromStructure(end.magnitude - start.magnitude + 1)")
  _external_vals = dict(PSObjectFromStructure=PSObjectFromStructure)
  _guessers = ('start: instance.items[0]',
               'end: instance.items[-1]',
               # Handles the case where we have an empty list
               'length: PSObjectFromStructure(len(instance.items))',
               'start: PSObjectFromStructure(1)')

  def __init__(self):
    self._object_constructors = {('start', 'end'): self.CreateFromStartAndEnd  }
    PyCategory.__init__(self)

  def CreateFromStartAndEnd(self, start, end):
    return PSObjectFromStructure(tuple(range(start.magnitude, end.magnitude + 1)))

  def BriefLabel(self):
    return "BasicSuccessorCategory"


class BasicPredecessorCategory(PyCategory):
  """Category of items such as (4, 3, 2)"""

  _rules = ("end: PSObjectFromStructure(start.magnitude - length.magnitude + 1)",
            "start: PSObjectFromStructure(end.magnitude + length.magnitude - 1)",
            "length: PSObjectFromStructure(start.magnitude - end.magnitude + 1)")
  _external_vals = dict(PSObjectFromStructure=PSObjectFromStructure)
  _guessers = ('start: instance.items[0]',
               'end: instance.items[-1]',
               # Handles the case where we have an empty list
               'length: PSObjectFromStructure(len(instance.items))',
               'start: PSObjectFromStructure(1)')

  def __init__(self):
    self._object_constructors = {('start', 'end'): self.CreateFromStartAndEnd  }
    PyCategory.__init__(self)

  def CreateFromStartAndEnd(self, start, end):
    return PSObjectFromStructure(tuple(range(start.magnitude, end.magnitude - 1, -1)))

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

    self._guessers = ('whole: instance', )
    self._external_vals = dict(PSGroup=PSGroup, Verify=logic.Verify,
                               len=len, all=all, tuple=tuple, x=0, base_cat=base_category,
                               PSObjectFromStructure=PSObjectFromStructure)
    rules = []
    rules.append('length: PSObjectFromStructure(len(whole.items))')
    rules.append('start: whole.items[0]')
    rules.append('end: whole.items[-1]')
    rules.append('whole: Verify(whole, all(x.DescribeAs(base_cat) for x in whole.items))')
    for att, att_cat in attribute_categories:
      att_var = 'att_%s' % att
      att_cat_var = 'att_cat__%s' % att
      self._external_vals[att_cat_var] = att_cat
      new_rule = '%s: PSGroup(items=tuple(x.DescribeAs(base_cat).GetAttributeOrNone(attribute="%s") for x in whole.items))' % (att_var, att)
      rules.append(new_rule)
      rules.append('%s: Verify(%s, %s.DescribeAs(%s))' % (att_var, att_var, att_var, att_cat_var))
    self._rules = tuple(rules)
    self._object_constructors = { ('whole', ): (lambda whole: whole)}
    PyCategory.__init__(self)

  def BriefLabel(self):
    return "CompoundCategory(%s: %s)" % (self.base_category.BriefLabel(),
                                         ', '.join("%s=%s" % (k, v.BriefLabel())
                                                   for k, v in self.attribute_categories))
