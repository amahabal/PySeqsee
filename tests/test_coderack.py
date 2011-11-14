import unittest
from components.coderack import Coderack, CoderackEmptyException

from farg.codelet import Codelet, CodeletFamily
from farg.exceptions import FargError

class RunState(object):
  def __init__(self):
    self.x = 5

class Foo(CodeletFamily):
  @classmethod
  def Run(cls, runstate, x):
    runstate.x *= 3
    return x + runstate.x

class TestCoderack(unittest.TestCase):
  def test_basic(self):
    c = Coderack(10)
    runstate = RunState()
    codelet = Codelet(Foo, runstate, 20, x=3)

    assert 10 == c._max_capacity
    c.AddCodelet(codelet)
    assert 1 == c._codelet_count
    assert 20 == c._urgency_sum

    c._ExpungeSomeCodelet()
    assert 0 == c._codelet_count
    assert 0 == c._urgency_sum

    self.assertRaises(CoderackEmptyException, c.GetCodelet)

  def test_force_next_codelet(self):
    """For testing, it is useful to mark the next codelet that GetCodelet() returns."""
    c = Coderack(10)
    runstate = RunState()
    codelet = Codelet(Foo, runstate, 20, x=3)
    codelet2 = Codelet(Foo, runstate, 30, x=4)
    codelet3 = Codelet(Foo, runstate, 30, x=4)

    c.AddCodelet(codelet)
    c.AddCodelet(codelet2)

    self.assertEqual(None, c._forced_next_codelet)
    self.assertRaises(FargError, c.ForceNextCodelet, codelet3)  # Not in coderack

    c.ForceNextCodelet(codelet2)
    self.assertEqual(codelet2, c._forced_next_codelet)

    self.assertEqual(codelet2, c.GetCodelet())
    self.assertEqual(None, c._forced_next_codelet)

    self.assertRaises(FargError, c.ForceNextCodelet, codelet2)  # Not in coderack any longer.

