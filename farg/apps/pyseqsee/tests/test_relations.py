import unittest
from farg.apps.pyseqsee.utils import PSObjectFromStructure
from farg.apps.pyseqsee.relation import PSRelation
from farg.apps.pyseqsee.categorization.categories import PyCategory

class TestRelations(unittest.TestCase):

  def test_sanity(self):
    o1 = PSObjectFromStructure(4)
    o2 = PSObjectFromStructure(8)

    # This creates a relationship with no categories. We can call DescribeAs() with various relation
    # types.
    r = o1.GetRelationTo(o2)
    self.assertIsInstance(r, PSRelation)
    self.assertEqual(o1, r.first)
    self.assertEqual(o2, r.second)

    self.assertEqual(r, o1.GetRelationTo(o2), "You get back the same relation")
    self.assertNotEqual(r, o2.GetRelationTo(o1), "Not the same relation in the reverse direction")

    self.assertIsInstance(o1.GetRelationTo(o1), PSRelation, "Self relations are fine")

  def test_reln_cat(self):

    class SameStructureReln(PyCategory):
      _Checks = ('_INSTANCE.first.Structure() == _INSTANCE.second.Structure()', )

    o1 = PSObjectFromStructure(4)
    o2 = PSObjectFromStructure(8)
    o3 = PSObjectFromStructure(4)
    r_12 = o1.GetRelationTo(o2)
    r_13 = o1.GetRelationTo(o3)
    self.assertTrue(r_13.DescribeAs(SameStructureReln()))
    self.assertFalse(r_12.DescribeAs(SameStructureReln()))
