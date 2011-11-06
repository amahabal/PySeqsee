"""Seqsee-specific categories."""

from farg.category import Binding, Category
from apps.seqsee.sobject import SAnchored, SElement, SObject


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

