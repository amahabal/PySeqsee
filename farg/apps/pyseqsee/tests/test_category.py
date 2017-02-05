import unittest
from farg.apps.pyseqsee.arena import PSArena
from farg.apps.pyseqsee import categories as C
from farg.apps.pyseqsee.objects import PSGroup

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
    c1 = C.CategoryEvenInteger()
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

class TestMultipartCategory(unittest.TestCase):
  """Here we test the 2-part category where the first part is 3, the other part is a number."""

  def test_creation(self):
    self.assertRaises(C.BadCategorySpec,
                      C.MultiPartCategory,
                      parts_count=0, part_categories=None)
    self.assertRaises(C.BadCategorySpec,
                      C.MultiPartCategory,
                      parts_count=2,  part_categories=(C.CategoryAnyObject()))
    c1 = C.MultiPartCategory(parts_count = 2, part_categories=(C.CategoryEvenInteger(),
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

##################### EXPLORATORY BELOW THIS POINT. ALL TESTS BELOW ARE MARKED SKIPPED


class TestSamenessCategory(unittest.TestCase):

  @unittest.skip("Not yet implemented")
  def test_creation(self):
    c1 = CategorySameness()
    c2 = CategorySameness()
    self.assertEqual(c1, c2, "CategorySameness is memoized")

    arena = PSArena(magnitudes=(7, 7, 7, 7, 7, 7, 7, 7, 7, 7))
    gp = PSGroup(items=arena.element[2:5]) # 7 7 7
    logic = gp.DescribeAs(c1)
    self.assertTrue(logic)

    self.assertTrue(logic.GroupCanBeExtended(), "This group can be extended")
    self.assertFalse(logic.IsDegenerate(), "7 7 7 is not degenerate")

    gp2 = PSGroup(items=(arena.element[2], )) # 7 7 7
    logic2 = gp2.DescribeAs(c1)
    self.assertTrue(logic2)
    self.assertTrue(logic2.GroupCanBeExtended(), "This group can be extended")
    self.assertTrue(logic2.IsDegenerate(), "7, by itself, *is* degenerate")

  @unittest.skip("Not yet implemented")
  def test_abstract_version(self):
    """Sameness can be based on the abstract notion of equivalence of some category.

    Looked at this way, the case above is a very special, literal, equivalence. Less literal are
    categories where instances are made of three groups, each a sameness group, and all are the
    same length. Thus, ((1 1)(7 7)(9 9)) is an instance, but these two are not ((5 5)(6 6)(7 7 7))
    or ((5 6)(5 6)(5 6)).
    """
    pass



