"""Defines the categories for objects."""
from farg.apps.pyseqsee.categorization import logic
from farg.apps.pyseqsee.categorization.logic import ConditionalValue
from farg.apps.pyseqsee.objects import PSElement, PSGroup
from farg.apps.pyseqsee.utils import PSObjectFromStructure
PSCategory = logic.PSCategory


class BadCategorySpec(Exception):
  """Raised when the specification for creating a category is somehow wrong.

  Note that this is different from the exception raised when creating instances
  of categories.
  """
  pass


class CategoryAnyObject(PSCategory):
  _Rules = ('_it: _INSTANCE',)
  _Constructors = {('_it',): (lambda _it: _it)}

  def BriefLabel(self):
    return 'CategoryAnyObject'


class MultiPartCategory(PSCategory):
  """Category whose instances are made up of N different parts.

  Each part can specify its own category.
  """

  def __init__(self, *, parts_count, part_categories):
    if not isinstance(parts_count, int) or parts_count <= 0:
      raise BadCategorySpec('Strange parts_count')
    if not isinstance(part_categories,
                      tuple) or len(part_categories) != parts_count:
      raise BadCategorySpec('parts_count does not match part_categories')
    if not all(isinstance(x, PSCategory) for x in part_categories):
      raise BadCategorySpec('Saw a non-PSCategory as a category for a part')
    self.parts_count = parts_count
    self.part_categories = part_categories

    self._Attributes = tuple('part_%d' % (x + 1) for x in range(parts_count))
    self._Context = dict(PSGroup=PSGroup)
    rules = []
    checks = []
    for x in range(parts_count):
      var = 'part_%d' % (x + 1)
      cat_name = 'cat_%d' % (x + 1)
      checks.append('%s.DescribeAs(%s)' % (var, cat_name))
      rules.append('%s: _INSTANCE.items[%d]' % (var, x))
      self._Context[cat_name] = part_categories[x]
    self._Rules = tuple(rules)
    self._Checks = tuple(checks)

    def CreateGivenParts(**parts_def):
      parts = []
      for x in range(parts_count):
        parts.append(parts_def['part_%d' % (x + 1)])
      return PSGroup(items=parts)

    self._Constructors = {self._Attributes: CreateGivenParts}
    PSCategory.__init__(self)

  def BriefLabel(self):
    return 'MultiPartCategory(' + ', '.join(x.BriefLabel()
                                            for x in self.part_categories) + ')'


class RepeatedIntegerCategory(PSCategory):
  """Category of items such as (3, 3, 3, 3)."""

  _Attributes = ('magnitude', 'length')

  _Rules = ('_mag: _INSTANCE.items[0].magnitude',
            '_mag: ConditionalValue(_length == 0, 1)',
            '_mag: magnitude.magnitude', '_length: len(_INSTANCE.items)',
            '_length: length.magnitude', 'magnitude: PSElement(magnitude=_mag)',
            'length: PSElement(magnitude=_length)')
  _Context = dict(
      PSObjectFromStructure=PSObjectFromStructure,
      PSElement=PSElement,
      len=len,
      ConditionalValue=logic.ConditionalValue)

  def __init__(self):
    self._Constructors = {('_mag', '_length'): self.CreateFromMagAndLength}
    PSCategory.__init__(self)

  def CreateFromMagAndLength(self, _mag, _length):
    return PSObjectFromStructure((_mag,) * _length)

  def BriefLabel(self):
    return 'RepeatedIntegerCategory'

  def GetAffordanceForInstance(self, instance):
    return 1  # Fake, replace with something realer...


class BasicSuccessorCategory(PSCategory):
  """Category of items such as (2, 3, 4)"""

  _Attributes = ('end', 'start', 'length')
  _Rules = ('_end: end.magnitude', 'end: PSElement(magnitude=_end)',
            '_start: start.magnitude', 'start: PSElement(magnitude=_start)',
            '_length: length.magnitude', 'length: PSElement(magnitude=_length)',
            '_end: _start + _length - 1', '_start: _end - _length + 1',
            '_length: _end - _start + 1', '_end: _INSTANCE.items[-1].magnitude',
            '_start: _INSTANCE.items[0].magnitude',
            '_start: ConditionalValue(_length == 0, 1)',
            '_length: len(_INSTANCE.items)')
  _Checks = ('_end == _start + _length - 1',)
  _Context = dict(
      PSElement=PSElement,
      PSObjectFromStructure=PSObjectFromStructure,
      len=len,
      ConditionalValue=logic.ConditionalValue)

  def __init__(self):
    self._Constructors = {('_start', '_end'): self.CreateFromStartAndEnd}
    PSCategory.__init__(self)

  def CreateFromStartAndEnd(self, _start, _end):
    return PSObjectFromStructure(tuple(range(_start, _end + 1)))

  def BriefLabel(self):
    return 'BasicSuccessorCategory'


class BasicPredecessorCategory(PSCategory):
  """Category of items such as (4, 3, 2)"""

  _Attributes = ('end', 'start', 'length')
  _Rules = ('_end: end.magnitude', 'end: PSElement(magnitude=_end)',
            '_start: start.magnitude', 'start: PSElement(magnitude=_start)',
            '_length: length.magnitude', 'length: PSElement(magnitude=_length)',
            '_end: _start - _length + 1', '_start: _end + _length - 1',
            '_length: _start - _end + 1', '_end: _INSTANCE.items[-1].magnitude',
            '_start: _INSTANCE.items[0].magnitude',
            '_start: ConditionalValue(_length == 0, 1)',
            '_length: len(_INSTANCE.items)')
  _Checks = ('_end == _start - _length + 1',)
  _Context = dict(
      PSElement=PSElement,
      PSObjectFromStructure=PSObjectFromStructure,
      len=len,
      ConditionalValue=logic.ConditionalValue)

  def __init__(self):
    self._Constructors = {('_start', '_end'): self.CreateFromStartAndEnd}
    PSCategory.__init__(self)

  def CreateFromStartAndEnd(self, _start, _end):
    return PSObjectFromStructure(tuple(range(_start, _end - 1, -1)))

  def BriefLabel(self):
    return 'BasicPredecessorCategory'


class CompoundCategory(PSCategory):
  """Category for things such as ((7), (7, 8), (7, 8, 9)), where components are based on another category."""

  def __init__(self, *, base_category, attribute_categories):
    if not isinstance(base_category, PSCategory):
      raise BadCategorySpec('base_category must be a category')
    if not isinstance(attribute_categories, tuple):
      raise BadCategorySpec(
          'attribute_categories must be a tuple, with each item a (name, cat) '
          'pair'
      )
    if not all(
        isinstance(x, tuple) and len(x) == 2 and isinstance(x[1], PSCategory)
        for x in attribute_categories):
      raise BadCategorySpec(
          'attribute_categories must be a tuple, with each item a (name, cat) '
          'pair'
      )
    attributes = tuple(x[0] for x in attribute_categories)
    if attributes != tuple(sorted(attributes)):
      raise BadCategorySpec('Attributes must be sorted')
    self.base_category = base_category
    self.attribute_categories = attribute_categories

    cat_attributes = ['att_%s' % x for x in attributes]
    cat_attributes.append('length')
    cat_attributes.append('start')
    cat_attributes.append('end')

    self._Context = dict(
        PSGroup=PSGroup,
        base_cat=base_category,
        PSObjectFromStructure=PSObjectFromStructure,
        x=0,
        len=len,
        all=all,
        tuple=tuple)
    self._RequiredAttributes = set()
    rules = [
        '_length: len(_INSTANCE.items)', '_length: length.magnitude',
        'length: PSObjectFromStructure(_length)', 'start: _INSTANCE.items[0]',
        'end: _INSTANCE.items[-1]'
    ]
    checks = ['all(x.DescribeAs(base_cat) for x in _INSTANCE.items)']

    for att, att_cat in attribute_categories:
      att_var = 'att_%s' % att
      att_cat_var = 'att_cat__%s' % att
      self._Context[att_cat_var] = att_cat
      new_rule = ('%s: '
                  'PSGroup(items=tuple(x.DescribeAs(base_cat).GetAttributeOrNone(attribute="%s")'
                  ' for x in _INSTANCE.items))') % (
          att_var, att)
      rules.append(new_rule)
      self._RequiredAttributes.add(att_var)
      checks.append('%s.DescribeAs(%s)' % (att_var, att_cat_var))
    self._Rules = tuple(rules)
    self._Checks = tuple(checks)

    self._Constructors = {('_INSTANCE',): (lambda _INSTANCE: _INSTANCE)}

    self._Attributes = tuple(cat_attributes)
    PSCategory.__init__(self)

  def BriefLabel(self):
    return 'CompoundCategory(%s: %s)' % (
        self.base_category.BriefLabel(), ', '.join('%s=%s' % (
            k, v.BriefLabel()) for k, v in self.attribute_categories))
