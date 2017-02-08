import unittest
from farg.apps.pyseqsee.arena import PSArena
from farg.apps.pyseqsee.categorization import categories as C
from farg.apps.pyseqsee.objects import PSGroup
from farg.apps.pyseqsee.categorization.numeric import CategoryEvenInteger, CategoryPrime
from farg.apps.pyseqsee.tests.utils import CategoryTester, CategoryLogicTester
from farg.apps.pyseqsee.utils import PSObjectFromStructure

class TestCategoryAnyObject(unittest.TestCase):
  """Test the simplest category of all: any group or element whatsoever is an instance."""

  def test_creation(self):
    c1 = C.CategoryAnyObject()
    c2 = C.CategoryAnyObject()
    self.assertEqual(c1, c2, "CategoryAnyObject is memoized")

    tester = CategoryTester(
      positive=(),
      negative=())

    tester = CategoryTester(
      positive=( (2, 7), ),
      negative=())
    tester(self, c1)

    # Not much can be done with this category. But some things that we should be able to do is get
    # examples---a diverse set of examples---when needed. This category would not have any
    # affordances of its own. Categories should be able to confer strength on to instances: this
    # category would do no such thing.

class TestCategoryEvenInteger(unittest.TestCase):
  def test_creation(self):
    c1 = CategoryEvenInteger()
    tester = CategoryTester(
      positive=( 2, ),
      negative=( 9,
                 (2, ),
                 ()))
    tester(self, c1)

    # Not tested yet: one of the affordance of this category may be to "think of" what its half is,
    # or to create a derivative sequence containg halves. I have no idea as yet where the pressure
    # should come from.

class TestCategoryPrime(unittest.TestCase):
  def test_creation(self):
    c1 = CategoryPrime()
    tester = CategoryTester(
      positive=( 2, ),
      negative=( 9,
                 (2, ),
                 ()))
    tester(self, c1)

    def logic_tester(test, logic):
      test.assertTrue(logic)
      attributes = logic.Attributes()
      test.assertEqual(3, attributes['index'].magnitude)

    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure(7),
                       cat=c1,
                       tester=logic_tester)

    # It seems wrong to always return an index. Most times, when we recognize that something is a
    # prime, we do not know what its index is. We need a way to add those things on demand later,
    # instead of always finding the index. Plus, for things such as Fibonacci, where elements are
    # repeated, what "index" means becomes confusing.


class TestMultipartCategory(unittest.TestCase):
  """Here we test the 2-part category where the first part is 3, the other part is a number."""

  def test_creation(self):
    self.assertRaises(C.BadCategorySpec,
                      C.MultiPartCategory,
                      parts_count=0, part_categories=None)
    self.assertRaises(C.BadCategorySpec,
                      C.MultiPartCategory,
                      parts_count=2,  part_categories=(C.CategoryAnyObject()))
    c1 = C.MultiPartCategory(parts_count = 2, part_categories=(CategoryEvenInteger(),
                                                               C.CategoryAnyObject()))
    c2 = C.MultiPartCategory(parts_count = 2, part_categories=(CategoryEvenInteger(),
                                                               C.CategoryAnyObject()))
    self.assertEqual(c1, c2, "Memoized")

    tester = CategoryTester(
      positive=( (2, 8),
                 (8, (7, 8)) ),
      negative=( 9,
                 2,
                 (2, ),
                 ()))
    tester(self, c1)

    # Not tested yet: affordances here would not include attempting to expand the group. But wait:
    # If the last element is an expandible group, then instances can be extended. This is getting
    # interesting.
    # Plus, this would be a prime case for multiple logics for instancehood...

class TestRepeatedIntegerCategory(unittest.TestCase):
  def test_creation(self):
    c1 = C.RepeatedIntegerCategory()

    tester = CategoryTester(
      positive=( (2, 2),
                 (2, ),
                 () ),
      negative=( 9,
                 2,
                 (2, 3)))
    tester(self, c1)

    def logic_tester(mag, length):
      def impl(test, logic):
        test.assertTrue(logic)
        attributes = logic.Attributes()
        test.assertEqual(mag, attributes['magnitude'].magnitude)
        test.assertEqual(length, attributes['length'].magnitude)
      return impl

    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure((7, )),
                       cat=c1,
                       tester=logic_tester(7, 1))
    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure((8, 8, 8)),
                       cat=c1,
                       tester=logic_tester(8, 3))

    # This group *can* be extended... the affordance should indicate that.

class TestBasicSuccessorCategory(unittest.TestCase):
  def test_creation(self):
    c1 = C.BasicSuccessorCategory()

    tester = CategoryTester(
      positive=( (2, 3),
                 (2, ),
                 () ),
      negative=( 9,
                 2,
                 (2, 2),
                 (2, 3, 4, 6)))
    tester(self, c1)

    def logic_tester(start, end, length):
      def impl(test, logic):
        test.assertTrue(logic)
        attributes = logic.Attributes()
        if start is not None:
          test.assertEqual(start, attributes['start'].magnitude)
        if end is not None:
          test.assertEqual(end, attributes['end'].magnitude)
        test.assertEqual(length, attributes['length'].magnitude)
      return impl

    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure((7, )),
                       cat=c1,
                       tester=logic_tester(7, 7, 1))
    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure((8, 9, 10)),
                       cat=c1,
                       tester=logic_tester(8, 10, 3))
    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure(()),
                       cat=c1,
                       tester=logic_tester(None, None, 0))

class TestBasicPredecessorCategory(unittest.TestCase):
  def test_creation(self):
    c1 = C.BasicPredecessorCategory()
    arena = PSArena(magnitudes=(5, 4, 3, 1))
    just_int = arena.element[0]
    empty_gp = PSGroup(items=())
    singleton_gp = PSGroup(items=(arena.element[0], ))
    longer_gp = PSGroup(items=arena.element[0:3])
    mixed_gp = PSGroup(items=arena.element[0:4])

    self.assertFalse(just_int.DescribeAs(c1))
    self.assertFalse(mixed_gp.DescribeAs(c1))

    logic = singleton_gp.DescribeAs(c1)
    self.assertTrue(logic)
    logic2 = longer_gp.DescribeAs(c1)
    self.assertTrue(logic2)
    logic3 = empty_gp.DescribeAs(c1)
    self.assertTrue(logic3)

    attributes = logic.Attributes()
    self.assertEqual(5, attributes['start'].magnitude)
    self.assertEqual(5, attributes['end'].magnitude)
    self.assertEqual(1, attributes['length'].magnitude)

    attributes = logic2.Attributes()
    self.assertEqual(5, attributes['start'].magnitude)
    self.assertEqual(3, attributes['end'].magnitude)
    self.assertEqual(3, attributes['length'].magnitude)

    attributes = logic3.Attributes()
    self.assertEqual(0, attributes['length'].magnitude)

class TestCompoundCategory(unittest.TestCase):
  """Tests the category defined in terms of another category's logic."""
  def test_creation(self):
    c1 = C.CompoundCategory(base_category=C.BasicSuccessorCategory(),
                            attribute_categories=(('end', C.BasicSuccessorCategory()),
                                                  ('length', C.BasicSuccessorCategory()),
                                                  ('start', C.RepeatedIntegerCategory())))
    c2 = C.CompoundCategory(base_category=C.BasicSuccessorCategory(),
                            attribute_categories=(('end', C.BasicSuccessorCategory()),
                                                  ('length', C.BasicSuccessorCategory()),
                                                  ('start', C.RepeatedIntegerCategory())))
    self.assertEqual(c1, c2, "Cached properly")

    # In creation, attribute_categories must be sorted and contain categories.
    self.assertRaises(C.BadCategorySpec,
                      C.CompoundCategory,
                      base_category=C.BasicSuccessorCategory(),
                      attribute_categories=(('length', C.BasicSuccessorCategory()),
                                            ('end', C.BasicSuccessorCategory()),
                                            ('start', C.RepeatedIntegerCategory())))

    c3 = C.CompoundCategory(base_category=C.BasicSuccessorCategory(),
                            attribute_categories=(('end', C.BasicSuccessorCategory()),
                                                  ('length', C.RepeatedIntegerCategory()),
                                                  ('start', C.BasicSuccessorCategory())))
    self.assertNotEqual(c1, c3, "Different categories")

    arena1 = PSArena(magnitudes=(7, 7, 8, 7, 8, 9, 7, 8, 9, 10))
    arena2 = PSArena(magnitudes=(7, 8, 9, 8, 9, 10, 9, 10, 11))

    # Set up the group ((7), (7, 8), (7, 8, 9))
    gp_1_1 = PSGroup(items=arena1.element[0:1])
    gp_1_2 = PSGroup(items=arena1.element[1:3])
    gp_1_3 = PSGroup(items=arena1.element[3:6])
    gp_1 = PSGroup(items=(gp_1_1, gp_1_2, gp_1_3))

    # Set up the group ((7, 8, 9), (8, 9, 10), (9, 10, 11))
    gp_2_1 = PSGroup(items=arena2.element[0:3])
    gp_2_2 = PSGroup(items=arena2.element[3:6])
    gp_2_3 = PSGroup(items=arena2.element[6:9])
    gp_2 = PSGroup(items=(gp_2_1, gp_2_2, gp_2_3))

    self.assertFalse(gp_1.DescribeAs(c3), "gp1 is not a c3")
    self.assertFalse(gp_2.DescribeAs(c1), "gp2 is not a c1")

    logic1 = gp_1.DescribeAs(c1)
    self.assertTrue(logic1)
    attributes = logic1.Attributes()
    self.assertEqual(3, attributes['length'].magnitude)
    self.assertEqual((7,), attributes['start'].Structure())
    self.assertEqual((7, 8, 9), attributes['end'].Structure())

    logic2 = gp_2.DescribeAs(c3)
    self.assertTrue(logic2)
    attributes = logic2.Attributes()
    self.assertEqual(3, attributes['length'].magnitude)
    self.assertEqual((7, 8, 9), attributes['start'].Structure())
    self.assertEqual((9, 10, 11), attributes['end'].Structure())
