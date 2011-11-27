import unittest

from farg.codelet import Codelet, CodeletFamily

class Controller(object):
  def __init__(self):
    self.x = 5

class Foo(CodeletFamily):
  @classmethod
  def Run(cls, controller, x):
    controller.x *= 3
    return x + controller.x

class Test(unittest.TestCase):
  def test_sanity(self):
    controller = Controller()
    c = Codelet(Foo, controller, 50, x=3)
    self.assertEqual(50, c.urgency)
    self.assertEqual(18, c.Run())
    self.assertEqual(c, controller.most_recent_codelet)
    self.assertEqual(48, c.Run())
