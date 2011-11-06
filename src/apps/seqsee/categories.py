"""Seqsee-specific categories."""

from farg.category import Binding, Category
from apps.seqsee.sobject import SAnchored, SElement, SObject
from apps.seqsee.mapping import NumericMapping

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


class Prime(NumericCategory):
  primes_list = [int(x) for x in
                 '2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97'.split()]
  largest_prime = max(primes_list)

  @classmethod
  def NumericIsInstance(cls, val):
    try:
      index = Prime.primes_list.index(val)
      return Binding({'index': index})
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
    diff = index2 - index1
    if diff == 1:
      return NumericMapping("succ", Prime)
    elif diff == 0:
      return NumericMapping("same", Prime)
    elif diff == -1:
      return NumericMapping("pred", Prime)
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
