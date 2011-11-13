import unittest

from farg.codelet import Codelet, CodeletFamily

class RunState(object):
  def __init__(self):
    self.x = 5

class Foo(CodeletFamily):
  @classmethod
  def Run(cls, runstate, x):
    runstate.x *= 3
    return x + runstate.x

class Test(unittest.TestCase):
  def test_sanity(self):
    runstate = RunState()
    c = Codelet(Foo, runstate, 50, x=3)
    self.assertEqual(50, c.urgency)
    self.assertEqual(18, c.Run())
    self.assertEqual(48, c.Run())
