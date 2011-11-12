"""Seqsee-specific categories."""

from farg.category import Binding, Category
from apps.seqsee.sobject import SAnchored, SElement, SObject
from apps.seqsee.mapping import NumericMapping, StructuralMapping
from apps.seqsee.structure_utils import StructureDepth
from farg.exceptions import FargError

class NumericCategory(Category):
  """Base class for categories whose instances are SElements, and membership depends only on the
     magnitude.
  """
  @classmethod
  def IsInstance(cls, item):
    if not isinstance(item, SElement):
      return None
    magnitude = item.magnitude
    return cls.NumericIsInstance(magnitude)

class StructuralCategory(Category):
  """Base class whose membership depends on the structure (e.g., ascending, mountain)."""
  @classmethod
  def IsInstance(cls, item):
    return cls.StructuralIsInstance(item.Structure())

  @classmethod
  def GetMapping(cls, item1, item2):
    binding1 = item1.DescribeAs(cls)
    if not binding1: return None
    binding2 = item2.DescribeAs(cls)
    if not binding2: return None
    return cls.GetMappingBetweenBindings(binding1, binding2)

  @classmethod
  def GetMappingBetweenBindings(cls, binding1, binding2):
    """Get mapping between a pair of bindings. This should eventually be replaced by a space (as
    discussed in the last chapter of the dissertation). For now, I have a simple mechanism."""
    bindings_mapping = {}
    for k, v in binding1.bindings.iteritems():
      if k in binding2.bindings:
        v2 = binding2.bindings[k]
        possible_mapping = GetMapping(v, v2)
        if possible_mapping:
          bindings_mapping[k] = possible_mapping
    if cls.AreAttributesSufficientToBuild(bindings_mapping.keys()):
      return StructuralMapping(category=cls, bindings_mapping=bindings_mapping)
    return None

class Number(NumericCategory):
  def NumericIsInstance(cls, val):
    return Binding()

  @classmethod
  def GetMapping(cls, item1, item2):
    index1, index2 = item1.magnitude, item2.magnitude
    diff_string = NumericMapping.DifferenceString(index1, index2)
    if diff_string:
      return NumericMapping(diff_string, Number)
    else:
      return None

  @classmethod
  def ApplyMapping(cls, mapping, item):
    name = mapping.name
    if name == 'same':
      return item.DeepCopy()
    if name == 'pred':
      return SObject.Create(item.magnitude - 1)
    if name == 'succ':
      return SObject.Create(item.magnitude + 1)

class Prime(NumericCategory):
  primes_list = [int(x) for x in
                 '2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97'.split()]
  largest_prime = max(primes_list)

  @classmethod
  def NumericIsInstance(cls, val):
    try:
      index = Prime.primes_list.index(val)
      return Binding(index=index)
    except ValueError:
      return None

  @staticmethod
  def _NextPrime(val):
    if val >= Prime.largest_prime:
      return None
    return Prime.primes_list[Prime.primes_list.index(val) + 1]

  @staticmethod
  def _PrevPrime(val):
    if val <= 2:
      return None
    return Prime.primes_list[Prime.primes_list.index(val) - 1]

  @classmethod
  def GetMapping(cls, item1, item2):
    binding1 = item1.DescribeAs(cls)
    if not binding1: return None
    binding2 = item2.DescribeAs(cls)
    if not binding2: return None

    index1, index2 = binding1.GetBindingsForAttribute('index'), binding2.GetBindingsForAttribute('index')
    diff_string = NumericMapping.DifferenceString(index1, index2)
    if diff_string:
      return NumericMapping(diff_string, Prime)
    else:
      return None

  @classmethod
  def ApplyMapping(cls, mapping, item):
    name = mapping.name
    if name == 'same':
      return item.DeepCopy()
    if name == 'pred':
      val = Prime._PrevPrime(item.magnitude)
      if val:
        return SObject.Create(val)
      else:
        return None
    if name == 'succ':
      val = Prime._NextPrime(item.magnitude)
      if val:
        return SObject.Create(val)
      else:
        return None

class Ascending(StructuralCategory):

  @classmethod
  def StructuralIsInstance(cls, structure):
    depth = StructureDepth(structure)
    if depth >= 2: return None
    if depth == 0:
      return Binding(start=structure, end=structure, length=1)
    # So depth = 1
    for idx, v in enumerate(structure[1:], 1):
      if v != structure[idx - 1] + 1:
        return None
    return Binding(start=SObject.Create(structure[0]),
                   end=SObject.Create(structure[-1]))

  @classmethod
  def Create(cls, bindings):
    start = bindings.get('start', None)
    end = bindings.get('end', None)
    length = bindings.get('length', None)
    if not start:
      if not end or not length:
        raise FargError("Create called when attributes insufficient to build.")
      start_mag = end.magnitude - length.magnitude + 1
      return SObject.Create(list(range(start_mag, end.magnitude + 1)))
    if not end:
      if not start or not length:
        raise FargError("Create called when attributes insufficient to build.")
      end_mag = start.magnitude + length.magnitude - 1
      return SObject.Create(list(range(start.magnitude, end_mag + 1)))
    return SObject.Create(list(range(start.magnitude, end.magnitude + 1)))

  @classmethod
  def AreAttributesSufficientToBuild(cls, attributes):
    return len(set(attributes).intersection(set(['start', 'end', 'length']))) >= 2

def GetMapping(v1, v2):
  if isinstance(v1, int) and isinstance(v2, int):
    diff_string = NumericMapping.DifferenceString(v1, v2)
    if diff_string:
      return NumericMapping(diff_string, Number)
    else:
      return None
  common_categories = v1.GetCommonCategoriesSet(v2)
  if common_categories:
    # ... ToDo: Don't merely use the first category!
    cat = list(common_categories)[0]
    return cat.GetMapping(v1, v2)
  if isinstance(v1, SElement) and isinstance(v2, SElement):
    return GetMapping(v1.magnitude, v2.magnitude)
  return None

class CategoryFactory(object):
  memos = {}

  @classmethod
  def Create(cls, **kwargs):
    key = frozenset(kwargs.items())
    if key not in cls.memos:
      new_category = cls.Construct(**kwargs)
      cls.memos[key] = new_category
      return new_category
    return cls.memos[key]

class SizeNCategory(CategoryFactory):
  @classmethod
  def Construct(cls, size):
    if size == 1:
      raise FargError("Attempt to create a SizeN category with size=1")
    class SizeN(StructuralCategory):
      @classmethod
      def StructuralIsInstance(cls, structure):
        if isinstance(structure, int):
          return None
        if len(structure) != size:
          return None
        bindings = {}
        for idx, item in enumerate(structure, 1):
          bindings['pos_%d' % idx] = SObject.Create(item)
        return Binding(**bindings)

      @classmethod
      def AreAttributesSufficientToBuild(cls, attributes):
        for idx in range(1, size + 1):
          if 'pos_%d' % idx not in attributes:
            return False
        return True

      @classmethod
      def Create(cls, bindings):
        structure = [bindings['pos_%d' % x] for x in range(1, size + 1)]
        return SObject.Create(structure)
    return SizeN
