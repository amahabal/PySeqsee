import unittest
from farg.apps.pyseqsee.categorization import categories as C
from farg.apps.pyseqsee.utils import PSObjectFromStructure
from farg.apps.pyseqsee.categorization import logic
from farg.apps.pyseqsee.categorization.categories import PyCategory
from farg.apps.pyseqsee.tests.utils import CategoryLogicTester, StructureTester

def assert_creation(test, cat, expected, **kwargs):
  """Given a category and kwargs, tries to create an instance. Evaluates against expected."""
  instance = cat.CreateInstance(**kwargs)
  test.assertEqual(expected, instance.Structure())

def assert_creation_failure(test, cat, exception_type, **kwargs):
  """Given a category and kwargs, tries to create an instance. Evaluates against expected."""
  test.assertRaises(exception_type, cat.CreateInstance, **kwargs)

class TestCategoryLogic(unittest.TestCase):

  def test_argumentless_cat(self):
    class MyCat(PyCategory):

      _external_vals = dict(PSObjectFromStructure=PSObjectFromStructure)
      _rules = ("end: PSObjectFromStructure(start.magnitude + length.magnitude - 1)",
                "foo: PSObjectFromStructure((start.magnitude, end.magnitude))")
      _guessers = ("start: instance.items[0]", "end: instance.items[1].items[1]")

      def __init__(self):
        self._object_constructors = { ('foo', 'start'): self.ConstructFromFooAndStart }
        PyCategory.__init__(self)

      def ConstructFromFooAndStart(self, foo, start):
        return PSObjectFromStructure((start.magnitude, foo.Structure()))

    CategoryLogicTester(test=self,
                        item=PSObjectFromStructure( (7, (7, 11))),
                        cat=MyCat(),
                        tester=StructureTester(start=7, end=11, foo=(7, 11)))

    self.assertEqual(set(['end', 'start', 'length', 'foo']), MyCat().Attributes())

    self.assertEqual( (7, (7, 11)),
                      MyCat().CreateInstance(start=PSObjectFromStructure(7),
                                             length=PSObjectFromStructure(5)).Structure() )
    self.assertRaises(logic.InsufficientAttributesException,
                      MyCat().CreateInstance,
                      start=PSObjectFromStructure(7))

    self.assertEqual( (7, (7, 13)),
                      MyCat().CreateInstance(start=PSObjectFromStructure(7),
                                             end=PSObjectFromStructure(13)).Structure() )
    self.assertEqual( (7, (8, 11)),
                      MyCat().CreateInstance(start=PSObjectFromStructure(7),
                                             foo=PSObjectFromStructure((8, 11))).Structure() )

    self.assertRaises(logic.InconsistentAttributesException,
                      MyCat().CreateInstance,
                      start=PSObjectFromStructure(7),
                      end=PSObjectFromStructure(9),
                      foo=PSObjectFromStructure((7, 10)))

  def test_cat_with_arg(self):
    class MyCat(PyCategory):

      _external_vals = dict(PSObjectFromStructure=PSObjectFromStructure)
      _rules = ("length: NONE",
                "each: NONE")
      _guessers = ("length: PSObjectFromStructure(len(instance.items))", "each: instance.items[0]")

      def __init__(self, *, index_with_one):
        self.index_with_one = index_with_one
        self._object_constructors = { ('length', 'each'): self.ConstructFromLengthAndEach }
        PyCategory.__init__(self)

      def ConstructFromLengthAndEach(self, length, each):
        args = []
        for x in range(length.magnitude):
          if x == self.index_with_one:
            args.append(1)
          else:
            args.append(each.magnitude)
        return PSObjectFromStructure(tuple(args))

    CategoryLogicTester(test=self,
                        item=PSObjectFromStructure( (7, 7, 7, 1, 7) ),
                        cat=MyCat(index_with_one=3),
                        tester=StructureTester(each=7, length=5))


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

class TestRepeatedIntegerLogic(unittest.TestCase):
  def test_creation(self):
    """Test creation given attributes."""

    c1 = C.RepeatedIntegerCategory()

    assert_creation(self, c1, (6, 6, 6, 6),
                    magnitude=PSObjectFromStructure(6),
                    length=PSObjectFromStructure(4))

    assert_creation_failure(self, c1, logic.InsufficientAttributesException,
                            length=PSObjectFromStructure(8))
