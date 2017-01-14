import unittest
from farg.apps.seqsee.util import LessThan, LessThanEq, GreaterThan, GreaterThanEq, Exactly

class TestUtils(unittest.TestCase):
  def test_utility_functions(self):
    self.assertTrue(LessThan(3)(2), "2 is acceptable for the function LessThan(3)")
    self.assertTrue(LessThanEq(3)(2), "2 is acceptable for the function LessThanEq(3)")
    self.assertTrue(LessThanEq(3)(3))
    self.assertFalse(LessThan(3)(3))

    self.assertTrue(GreaterThan(3)(4))
    self.assertTrue(GreaterThanEq(3)(4))
    self.assertFalse(GreaterThan(3)(2))

    self.assertTrue(Exactly(3)(3))
    self.assertFalse(Exactly(3)(4))
