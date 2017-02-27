import unittest

from farg.apps.pyseqsee.arena import PSArena
from farg.apps.pyseqsee.categorization.categories import PSCategory
from farg.apps.pyseqsee.categorization.numeric import CategoryInteger
from farg.apps.pyseqsee.objects import PSElement
from farg.apps.pyseqsee.relation import PSRelation
from farg.apps.pyseqsee.utils import PSObjectFromStructure
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

    class SameStructureReln(PSCategory):
      _Checks = ('_INSTANCE.first.Structure() == _INSTANCE.second.Structure()', )

    o1 = PSObjectFromStructure(4)
    o2 = PSObjectFromStructure(8)
    o3 = PSObjectFromStructure(4)
    r_12 = o1.GetRelationTo(o2)
    r_13 = o1.GetRelationTo(o3)
    self.assertTrue(r_13.DescribeAs(SameStructureReln()))
    self.assertFalse(r_12.DescribeAs(SameStructureReln()))

  def test_reln_cat_with_arg(self):

    class DeltaReln(PSCategory):
      _Attributes = ('delta',)
      _RequiredAttributes = ('delta', )
      _Rules = ('delta: PSElement(magnitude=(_INSTANCE.second.magnitude - _INSTANCE.first.magnitude))',)
      _Checks = ('delta.magnitude == _INSTANCE.second.magnitude - _INSTANCE.first.magnitude', )
      _Context = dict(PSElement=PSElement)

    o1 = PSObjectFromStructure(4)
    o2 = PSObjectFromStructure(8)
    o3 = PSObjectFromStructure(4)
    r_12 = o1.GetRelationTo(o2)
    r_13 = o1.GetRelationTo(o3)
    l_12 = r_12.DescribeAs(DeltaReln())
    self.assertTrue(l_12)
    l_13 = r_13.DescribeAs(DeltaReln())
    self.assertTrue(l_13)
    self.assertEqual(4, l_12.Attributes()['delta'].magnitude)
    self.assertEqual(0, l_13.Attributes()['delta'].magnitude)

  def test_arena_merge(self):

    class SameStructureReln(PSCategory):
      _Checks = ('_INSTANCE.first.Structure() == _INSTANCE.second.Structure()', )

    gp = PSObjectFromStructure((5, 5))
    r = gp.items[0].GetRelationTo(gp.items[1])
    self.assertTrue(r.DescribeAs(SameStructureReln()))
    gp.SetSpanStart(0)
    a = PSArena(magnitudes=(5, 5, 5))
    r2 = gp.items[1].GetRelationTo(a.element[2])
    self.assertTrue(r2.DescribeAs(SameStructureReln()))

    self.assertFalse(a.element[0].GetRelationTo(a.element[1]).IsKnownAsInstanceOf(SameStructureReln()))
    self.assertFalse(a.element[1].GetRelationTo(a.element[2]).IsKnownAsInstanceOf(SameStructureReln()))

    a.MergeObject(gp)
    self.assertTrue(a.element[0].GetRelationTo(a.element[1]).IsKnownAsInstanceOf(SameStructureReln()))
    self.assertTrue(a.element[1].GetRelationTo(a.element[2]).IsKnownAsInstanceOf(SameStructureReln()))

  def test_find_reln(self):
    o1 = PSObjectFromStructure(4)
    o2 = PSObjectFromStructure(8)
    self.assertTrue(o1.IsKnownAsInstanceOf(CategoryInteger()))

    self.assertIn(CategoryInteger(), o1.CategoriesSharedWith(o2))
    r = o1.GetRelationTo(o2)
    r.FindCategories(end_category=CategoryInteger())
    self.assertTrue(r.IsKnownAsInstanceOf(CategoryInteger.DeltaReln()))
    self.assertEqual(4, r.DescribeAs(CategoryInteger.DeltaReln()).Attributes()['delta'].magnitude)
    self.assertTrue(r.IsKnownAsInstanceOf(CategoryInteger.RatioReln()))
    self.assertEqual(2, r.DescribeAs(CategoryInteger.RatioReln()).Attributes()['ratio'].magnitude)

    o3 = PSObjectFromStructure(3)
    o4 = PSObjectFromStructure(12)
    r2 = o3.GetRelationTo(o4)
    r2.FindCategoriesUsingEndCategories()
    self.assertEqual(9, r2.DescribeAs(CategoryInteger.DeltaReln()).Attributes()['delta'].magnitude)
    self.assertEqual(4, r2.DescribeAs(CategoryInteger.RatioReln()).Attributes()['ratio'].magnitude)
