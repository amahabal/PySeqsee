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

##################### EXPLORATORY BELOW THIS POINT. ALL TESTS BELOW ARE MARKED SKIPPED
class CategoryAdHocForTest(C.PyCategory):
  def __init__(self):
    pass

class TestCompoundCategory(unittest.TestCase):
  """Here we test the 2-part category where the first part is 3, the other part is a number."""

  @unittest.skip("Not yet implemented")
  def test_creation(self):
    c1 = CategoryAdHocForTest()  # Need a better name, and this should be defined here.

    arena = PSArena(magnitudes=(2, 7, 2, 8, 2, 9, 2, 10))
    gp1 = PSGroup(items=arena.element[1, 2])
    logic = gp1.DescribeAs(c1)
    self.assertIsNone(logic, "[7, 2] is not an instance")

    gp2 = PSGroup(items=arena.element[2, 3])
    logic = gp1.DescribeAs(c1)
    self.assertTrue(logic, "[2, 8] is an instance")

    self.assertFalse(logic.GroupCanBeExtended(), "This group cannot be extended")


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



