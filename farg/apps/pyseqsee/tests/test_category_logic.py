import unittest
from farg.apps.pyseqsee.categorization import categories as C
from farg.apps.pyseqsee.utils import PSObjectFromStructure
from farg.apps.pyseqsee.categorization.categories import InconsistentAttributesException,\
  InsufficientAttributesException
from farg.apps.pyseqsee.categorization.logic import AttributeInference as Inference

def assert_creation(test, cat, expected, **kwargs):
  """Given a category and kwargs, tries to create an instance. Evaluates against expected."""
  instance = cat.CreateInstance(**kwargs)
  test.assertEqual(expected, instance.Structure())

def assert_creation_failure(test, cat, exception_type, **kwargs):
  """Given a category and kwargs, tries to create an instance. Evaluates against expected."""
  test.assertRaises(exception_type, cat.CreateInstance, **kwargs)

class TestBasicSuccesorLogic(unittest.TestCase):

  def test_inference(self):
    rules = [Inference.Rule(target="end", expression="start.magnitude + length.magnitude - 1")]
    inference = Inference(rules)
    vals = dict(start=PSObjectFromStructure(7), length=PSObjectFromStructure(3), end=None)
    inference.RunInference(vals)
    self.assertEqual(vals["end"].magnitude, 9)

    vals = dict(start=PSObjectFromStructure(7), length=PSObjectFromStructure(3),
                end=PSObjectFromStructure(150))
    inference.RunInference(vals)
    self.assertEqual(vals["end"].magnitude, 150, "Not overwritten")
    self.assertFalse(inference.CheckConsistency(vals))

    vals = dict(start=PSObjectFromStructure(7), length=PSObjectFromStructure(3),
                end=PSObjectFromStructure(9))
    inference.RunInference(vals)
    self.assertEqual(vals["end"].magnitude, 9, "Not overwritten")
    self.assertTrue(inference.CheckConsistency(vals))

  def test_creation(self):
    """Test creation given attributes."""

    c1 = C.BasicSuccessorCategory()

    assert_creation(self, c1, (3, 4, 5, 6),
                    start=PSObjectFromStructure(3),
                    length=PSObjectFromStructure(4))

    assert_creation(self, c1, (3, 4, 5, 6, 7),
                    start=PSObjectFromStructure(3),
                    end=PSObjectFromStructure(7))

    assert_creation(self, c1, (2, 3, 4, 5, 6, 7),
                    end=PSObjectFromStructure(7),
                    length=PSObjectFromStructure(6))

    assert_creation(self, c1, (2, 3, 4, 5, 6, 7, 8),
                    end=PSObjectFromStructure(8),
                    length=PSObjectFromStructure(7),
                    start=PSObjectFromStructure(2))

    assert_creation_failure(self, c1, InconsistentAttributesException,
                            end=PSObjectFromStructure(8),
                            length=PSObjectFromStructure(7),
                            start=PSObjectFromStructure(4))

    assert_creation_failure(self, c1, InsufficientAttributesException,
                            end=PSObjectFromStructure(8))
