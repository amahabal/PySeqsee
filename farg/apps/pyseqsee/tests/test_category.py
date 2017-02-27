import unittest

from farg.apps.pyseqsee.arena import PSArena
from farg.apps.pyseqsee.categorization import categories as C
from farg.apps.pyseqsee.categorization.numeric import CategoryEvenInteger, CategoryPrime
from farg.apps.pyseqsee.objects import PSGroup
from farg.apps.pyseqsee.tests.utils import CategoryTester, CategoryLogicTester, StructureTester
from farg.apps.pyseqsee.utils import PSObjectFromStructure
class TestCategoryAnyObject(unittest.TestCase):
  """Test the simplest category of all: any group or element whatsoever is an instance."""

  def test_instancehood(self):
    c1 = C.CategoryAnyObject()
    c2 = C.CategoryAnyObject()
    self.assertEqual(c1, c2, "CategoryAnyObject is memoized")

    tester = CategoryTester(
      positive=( (2, 7), ),
      negative=())
    tester(self, c1)

    # Not much can be done with this category. But some things that we should be able to do is get
    # examples---a diverse set of examples---when needed. This category would not have any
    # affordances of its own. Categories should be able to confer strength on to instances: this
    # category would do no such thing.

class TestCategoryEvenInteger(unittest.TestCase):
  def test_instancehood(self):
    c1 = CategoryEvenInteger()
    tester = CategoryTester(
      positive=( 2, ),
      negative=( 9,
                 (2, ),
                 ()))
    tester(self, c1)

  def test_extra_attribs(self):
    c1 = CategoryEvenInteger()
    o1 = PSObjectFromStructure(4)
    l = o1.DescribeAs(c1)
    self.assertTrue(l)
    self.assertNotIn('half', l.Attributes(), "No attribute 'half' yet")

    c1.TurnOnAttribute('half')
    o2 = PSObjectFromStructure(6)
    l2 = o2.DescribeAs(c1)
    self.assertTrue(l2)
    self.assertIn('half', l2.Attributes(), "Attribute 'half' now present")
    self.assertEqual(3, l2.GetAttributeOrNone(attribute='half').magnitude)

    # Not tested yet: one of the affordance of this category may be to "think of" what its half is,
    # or to create a derivative sequence containg halves. I have no idea as yet where the pressure
    # should come from.

class TestCategoryPrime(unittest.TestCase):
  def test_instancehood(self):
    c1 = CategoryPrime()
    tester = CategoryTester(
      positive=( 2, ),
      negative=( 9,
                 (2, ),
                 ()))
    tester(self, c1)

    # It seems wrong to always return an index. Most times, when we recognize that something is a
    # prime, we do not know what its index is. We need a way to add those things on demand later,
    # instead of always finding the index. Plus, for things such as Fibonacci, where elements are
    # repeated, what "index" means becomes confusing.


class TestMultipartCategory(unittest.TestCase):
  """Here we test the 2-part category where the first part is 3, the other part is a number."""

  def test_instancehood(self):
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
  def test_instancehood(self):
    c1 = C.RepeatedIntegerCategory()

    tester = CategoryTester(
      positive=( (2, 2),
                 (2, ),
                 () ),
      negative=( 9,
                 2,
                 (2, 3)))
    tester(self, c1)

    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure((7, )),
                       cat=c1,
                       tester=StructureTester(magnitude=7, length=1))
    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure((8, 8, 8)),
                       cat=c1,
                       tester=StructureTester(magnitude=8, length=3))

  def test_categories_on_logic(self):
    c1 = C.RepeatedIntegerCategory()
    o1 = PSObjectFromStructure((7, 7))
    self.assertTrue(o1.DescribeAs(c1))
    self.assertTrue(o1.IsKnownAsInstanceOf(c1))

    logic = o1.DescribeAs(c1)
    logic.Attributes()['magnitude'].DescribeAs(CategoryPrime())
    self.assertTrue(logic.Attributes()['magnitude'].IsKnownAsInstanceOf(CategoryPrime()))

    # Get it again, see that the inner categorization has "stuck".
    logic = o1.DescribeAs(c1)
    self.assertTrue(logic.Attributes()['magnitude'].IsKnownAsInstanceOf(CategoryPrime()))

  def test_affordance(self):
    """What codelets does this suggest? It can own the relevant codelet families...

    This test is currently very speculative, as I try to firm up the interface a bit."""
    c1 = C.RepeatedIntegerCategory()
    o1 = PSObjectFromStructure((7, 7))
    self.assertTrue(o1.DescribeAs(c1))

    affordances = c1.GetAffordanceForInstance(o1)
    self.assertTrue(affordances)  # This is currently fake...

  # This group *can* be extended... the affordance should indicate that.

class TestBasicSuccessorCategory(unittest.TestCase):
  def test_instancehood(self):
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

    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure((7, )),
                       cat=c1,
                       tester=StructureTester(start=7, end=7, length=1))
    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure((8, 9, 10)),
                       cat=c1,
                       tester=StructureTester(start=8, end=10, length=3))
    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure(()),
                       cat=c1,
                       tester=StructureTester(length=0))

class TestBasicPredecessorCategory(unittest.TestCase):
  def test_instancehood(self):
    c1 = C.BasicPredecessorCategory()
    tester = CategoryTester(
      positive=( (3, 2),
                 (2, ),
                 () ),
      negative=( 9,
                 2,
                 (2, 2),
                 (6, 5, 4, 2)))
    tester(self, c1)

    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure((7, )),
                       cat=c1,
                       tester=StructureTester(start=7, end=7, length=1))
    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure((8, 7, 6)),
                       cat=c1,
                       tester=StructureTester(start=8, end=6, length=3))
    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure(()),
                       cat=c1,
                       tester=StructureTester(length=0))

class TestCompoundCategory(unittest.TestCase):
  """Tests the category defined in terms of another category's logic."""
  def test_instancehood(self):
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


    tester = CategoryTester(
      positive=( ((2, 3), (2, 3, 4), (2, 3, 4, 5)),
                 ((2, 3),),
                 ((2, ),),
                 ()),
      negative=( 9,
                 2,
                 (2, 3),
                 ((2, 3), (3, 4)),
                 ((2, 3), (2, 3, 4), (2, 3, 4, 5, 6))))
    tester(self, c1)

    tester = CategoryTester(
      positive=( ((2, 3), (3, 4), (4, 5)),
                 ((2, 3),),
                 ((2, ),),
                 () ),
      negative=( 9,
                 2,
                 (2, 3),
                 ((2, 3), (2, 3, 4)),
                 ((2, 3), (2, 3, 4), (2, 3, 4, 5, 6))))
    tester(self, c3)

    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure(((7, ), )),
                       cat=c1,
                       tester=StructureTester(start=(7, ), end=(7, ), length=1))
    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure(((7, 8), (7, 8, 9), (7, 8, 9, 10))),
                       cat=c1,
                       tester=StructureTester(start=(7, 8), end=(7, 8, 9, 10), length=3))
    CategoryLogicTester(test=self,
                       item=PSObjectFromStructure(()),
                       cat=c1,
                       tester=StructureTester(length=0))
