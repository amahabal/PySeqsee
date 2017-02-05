import unittest
from farg.apps.pyseqsee.arena import PSArena
from farg.apps.pyseqsee.categorization import categories as C
from farg.apps.pyseqsee.objects import PSGroup
from farg.apps.pyseqsee.categorization.numeric import CategoryEvenInteger, CategoryPrime

class TestCategoryAnyObject(unittest.TestCase):
  """Test the simplest category of all: any group or element whatsoever is an instance."""

  def test_creation(self):
    c1 = C.CategoryAnyObject()
    c2 = C.CategoryAnyObject()
    self.assertEqual(c1, c2, "CategoryAnyObject is memoized")

    arena = PSArena(magnitudes=(2, 7, 2, 8, 2, 9, 2, 10))
    gp1 = PSGroup(items=arena.element[1:3])
    logic = gp1.DescribeAs(c1)
    self.assertTrue(logic, "Description was successful")

    # Not much can be done with this category. But some things that we should be able to do is get
    # examples---a diverse set of examples---when needed. This category would not have any
    # affordances of its own. Categories should be able to confer strength on to instances: this
    # category would do no such thing.

class TestCategoryEvenInteger(unittest.TestCase):
  def test_creation(self):
    c1 = CategoryEvenInteger()
    arena = PSArena(magnitudes=(2, 7, 2, 8, 2, 9, 2, 10))
    elt_even = arena.element[4]  # This is 2
    elt_odd = arena.element[5]  # This is 9
    gp1 = PSGroup(items=arena.element[1:3])
    gp2 = PSGroup(items=(arena.element[4], ))

    self.assertFalse(elt_odd.DescribeAs(c1), "Not an instance: odd number")
    self.assertFalse(gp1.DescribeAs(c1), "Not an instance: multipart gp")
    self.assertFalse(gp2.DescribeAs(c1), "Not an instance: singleton group containing even")

    logic = elt_even.DescribeAs(c1)
    self.assertTrue(logic)

    # Not tested yet: one of the affordance of this category may be to "think of" what its half is,
    # or to create a derivative sequence containg halves. I have no idea as yet where the pressure
    # should come from.

class TestCategoryPrime(unittest.TestCase):
  def test_creation(self):
    c1 = CategoryPrime()
    arena = PSArena(magnitudes=(2, 7, 2, 8, 2, 9, 2, 10))
    elt_prime = arena.element[1]  # This is 7
    elt_comp = arena.element[5]  # This is 9
    gp1 = PSGroup(items=arena.element[1:3])
    gp2 = PSGroup(items=(arena.element[4], ))

    self.assertFalse(elt_comp.DescribeAs(c1), "Not an instance: composite number")
    self.assertFalse(gp1.DescribeAs(c1), "Not an instance: multipart gp")
    self.assertFalse(gp2.DescribeAs(c1), "Not an instance: singleton group containing even")

    logic = elt_prime.DescribeAs(c1)
    self.assertTrue(logic)
    attributes = logic.Attributes()
    self.assertEqual(3, attributes['index'])

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

    arena = PSArena(magnitudes=(2, 7, 2, 8, 2, 9, 2, 10))
    elt_even = arena.element[4]  # This is 2
    elt_odd = arena.element[5]  # This is 9
    gp1 = PSGroup(items=arena.element[2:4])  # This is (2, 8): Is an instance
    gp2 = PSGroup(items=arena.element[1:3])  # This is (7, 2): Not an instance

    self.assertFalse(elt_odd.DescribeAs(c1), "Not an instance: odd number")
    self.assertFalse(elt_even.DescribeAs(c1), "Not an instance: even number")
    self.assertFalse(gp2.DescribeAs(c1), "Not an instance: first part not even")

    logic = gp1.DescribeAs(c1)
    self.assertTrue(logic)

    # Not tested yet: affordances here would not include attempting to expand the group. But wait:
    # If the last element is an expandible group, then instances can be extended. This is getting
    # interesting.
    # Plus, this would be a prime case for multiple logics for instancehood...

class TestRepeatedIntegerCategory(unittest.TestCase):
  def test_creation(self):
    c1 = C.RepeatedIntegerCategory()
    arena = PSArena(magnitudes=(1, 1, 1, 2, 2, 2, 2, 3))
    just_int = arena.element[0]
    singleton_gp = PSGroup(items=(arena.element[0], ))
    longer_gp = PSGroup(items=arena.element[0:3])
    mixed_gp = PSGroup(items=arena.element[0:4])

    self.assertFalse(just_int.DescribeAs(c1))
    self.assertFalse(mixed_gp.DescribeAs(c1))

    logic = singleton_gp.DescribeAs(c1)
    self.assertTrue(logic)
    logic2 = longer_gp.DescribeAs(c1)
    self.assertTrue(logic2)

    attributes = logic.Attributes()
    self.assertEqual(1, attributes['magnitude'])
    self.assertEqual(1, attributes['length'])

    attributes = logic2.Attributes()
    self.assertEqual(1, attributes['magnitude'])
    self.assertEqual(3, attributes['length'])

    # This group *can* be extended... the affordance should indicate that.
