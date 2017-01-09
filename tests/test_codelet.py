import unittest

from farg.core.controller import Controller
from farg.core.codelet import Codelet, CodeletFamily

class MyController(Controller):
  def __init__(self):
    self.x = 5

class Foo(CodeletFamily):
  @classmethod
  def Run(cls, controller, x):
    controller.x *= 3
    return x + controller.x

class Test(unittest.TestCase):
  def test_sanity(self):
    controller = MyController()
    c = Codelet(Foo, controller, 50, dict(x=3))
    self.assertEqual(50, c.urgency)
    self.assertEqual(18, c.Run())
    self.assertEqual(c, controller.most_recent_codelet)
    self.assertEqual(48, c.Run())
