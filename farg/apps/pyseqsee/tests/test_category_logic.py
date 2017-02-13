import unittest
from farg.apps.pyseqsee.categorization import categories as C
from farg.apps.pyseqsee.utils import PSObjectFromStructure
from farg.apps.pyseqsee.categorization import logic

def assert_creation(test, cat, expected, **kwargs):
  """Given a category and kwargs, tries to create an instance. Evaluates against expected."""
  instance = cat.CreateInstance(**kwargs)
  test.assertEqual(expected, instance.Structure())

def assert_creation_failure(test, cat, exception_type, **kwargs):
  """Given a category and kwargs, tries to create an instance. Evaluates against expected."""
  test.assertRaises(exception_type, cat.CreateInstance, **kwargs)

class TestCategoryLogic(unittest.TestCase):
  def test_inference(self):

    def ConstructFromFooAndStart(foo, start):
      return PSObjectFromStructure((start.magnitude, foo.Structure()))

    class MyLogic(logic.CategoryLogic):
      external_vals = dict(PSObjectFromStructure=PSObjectFromStructure)
      object_constructors = { ('foo', 'start'): ConstructFromFooAndStart }
      rules = ("end: PSObjectFromStructure(start.magnitude + length.magnitude - 1)",
               "foo: PSObjectFromStructure((start.magnitude, end.magnitude))")

    class MyLogic2(logic.CategoryLogic):
      external_vals = dict(PSObjectFromStructure=PSObjectFromStructure)
      object_constructors = { ('foo', 'start'): ConstructFromFooAndStart }
      rules = ("end: PSObjectFromStructure(start.magnitude + length.magnitude - 1)",
               "foo: PSObjectFromStructure((start.magnitude, end.magnitude))")

    self.assertFalse(MyLogic._initialized)
    self.assertFalse(MyLogic2._initialized)
    MyLogic2.Initialize()
    self.assertFalse(MyLogic._initialized)
    self.assertTrue(MyLogic2._initialized)

    self.assertEqual(set(['end', 'start', 'length', 'foo']), MyLogic.Attributes())

    self.assertEqual( (7, (7, 11)),
                      MyLogic.Construct(start=PSObjectFromStructure(7),
                                        length=PSObjectFromStructure(5)).Structure() )
    self.assertRaises(logic.InsufficientAttributesException,
                      MyLogic.Construct,
                      start=PSObjectFromStructure(7))

    self.assertEqual( (7, (7, 13)),
                      MyLogic.Construct(start=PSObjectFromStructure(7),
                                               end=PSObjectFromStructure(13)).Structure() )
    self.assertEqual( (7, (8, 11)),
                      MyLogic.Construct(start=PSObjectFromStructure(7),
                                               foo=PSObjectFromStructure((8, 11))).Structure() )

    self.assertRaises(logic.InconsistentAttributesException,
                      MyLogic.Construct,
                      start=PSObjectFromStructure(7),
                      end=PSObjectFromStructure(9),
                      foo=PSObjectFromStructure((7, 10)))


class TestBasicSuccesorLogic(unittest.TestCase):

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

    assert_creation_failure(self, c1, logic.InconsistentAttributesException,
                            end=PSObjectFromStructure(8),
                            length=PSObjectFromStructure(7),
                            start=PSObjectFromStructure(4))

    assert_creation_failure(self, c1, logic.InsufficientAttributesException,
                            end=PSObjectFromStructure(8))

class TestBasicPredecesorLogic(unittest.TestCase):

  def test_creation(self):
    """Test creation given attributes."""

    c1 = C.BasicPredecessorCategory()

    assert_creation(self, c1, (6, 5, 4, 3),
                    start=PSObjectFromStructure(6),
                    length=PSObjectFromStructure(4))

    assert_creation(self, c1, (7, 6, 5, 4, 3),
                    start=PSObjectFromStructure(7),
                    end=PSObjectFromStructure(3))

    assert_creation(self, c1, (7, 6, 5, 4, 3, 2),
                    end=PSObjectFromStructure(2),
                    length=PSObjectFromStructure(6))

    assert_creation(self, c1, (8, 7, 6, 5, 4, 3, 2),
                    end=PSObjectFromStructure(2),
                    length=PSObjectFromStructure(7),
                    start=PSObjectFromStructure(8))

    assert_creation_failure(self, c1, logic.InconsistentAttributesException,
                            end=PSObjectFromStructure(8),
                            length=PSObjectFromStructure(7),
                            start=PSObjectFromStructure(4))

    assert_creation_failure(self, c1, logic.InsufficientAttributesException,
                            end=PSObjectFromStructure(8))
