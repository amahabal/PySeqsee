import unittest
from farg.apps.pyseqsee.stream import PSStream, PSFocusable
from farg.apps.pyseqsee.categorization.categorizable import Categorizable
from farg.apps.pyseqsee.categorization.logic import PSCategory
from farg.apps.pyseqsee.objects import PSElement
from farg.apps.pyseqsee.tests.utils import FringeTest

class TestFocusable(unittest.TestCase):
  def test_sanity(self):
    class F1(PSFocusable):
      def __init__(self, x):
        self.x = x
        PSFocusable.__init__(self)

      def CalculateFringe(self):
        """This fringe will be appended with a fringe coming from category membership."""
        return {self.x: 1.0, (self.x + 1): 0.5, (self.x - 1): 0.5}

    class FakeAttributeRichCategory(PSCategory):
      _Attributes = ('att_1', 'att_2', 'att_3')
      _Rules = ('att_1: PSElement(magnitude=1)', 'att_2: PSElement(magnitude=2)',
                'att_3: PSElement(magnitude=3)')
      _Context = dict(PSElement=PSElement)

    item = F1(3)
    self.assertIsInstance(item, Categorizable, "Focusables are categorizable")
    FringeTest(test=self, item=item, expected_fringe_parts=(2, 3, 4))
    fringe = item.GetFringe()
    self.assertEqual(item.stored_fringe, fringe, "Fringe is stored")
    self.assertTrue(item.DescribeAs(FakeAttributeRichCategory()))
    FringeTest(test=self, item=item,
               expected_fringe_parts=(2, 3, 4, FakeAttributeRichCategory(),
                                      (FakeAttributeRichCategory(), 'att_1', 1),
                                      (FakeAttributeRichCategory(), 'att_2', 2),
                                      (FakeAttributeRichCategory(), 'att_3', 3)))


class TestStream(unittest.TestCase):
  def test_creation(self):
    stream = PSStream()

