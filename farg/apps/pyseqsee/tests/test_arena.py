import unittest
from farg.apps.pyseqsee.arena import PSArena, ElementBeyondKnownSoughtException,\
  CannotInsertGroupWithoutSpans, UnmergableObjectException, ElementWayBeyondKnownSoughtException
from farg.apps.pyseqsee.objects import PSGroup, PSElement
from farg.apps.pyseqsee.utils import PSObjectFromStructure
from farg.apps.pyseqsee.categorization.numeric import CategoryPrime


class TestPSArena(unittest.TestCase):

  def test_basic(self):
    arena = PSArena(magnitudes=range(10))
    self.assertIsInstance(arena.element[0], PSElement)
    self.assertEqual(10, arena.Size())
    self.assertEqual((3, 3), arena.element[3].Span())

    arena.Append(magnitudes=(15, 160))
    self.assertEqual(12, arena.Size())
    self.assertEqual((11, 11), arena.element[11].Span())
    self.assertEqual(160, arena.element[11].magnitude)

    gp = PSGroup(items=arena.element[2:5])
    self.assertTrue(gp.InferSpans())
    self.assertEqual((2, 4), gp.Span())

  def test_with_offset(self):
    arena = PSArena(magnitudes=range(10), start=5)
    self.assertIsInstance(arena.element[0], PSElement)
    self.assertEqual(10, arena.Size())
    self.assertEqual((8, 8), arena.element[3].Span())

    arena.Append(magnitudes=(15, 160))
    self.assertEqual(12, arena.Size())
    self.assertEqual((16, 16), arena.element[11].Span())
    self.assertEqual(160, arena.element[11].magnitude)

    gp = PSGroup(items=arena.element[2:5])
    self.assertTrue(gp.InferSpans())
    self.assertEqual((7, 9), gp.Span())

    self.assertTrue(arena.CheckTerms(start=7, magnitudes=(2, 3, 4)))
    self.assertTrue(arena.CheckTerms(start=16, magnitudes=(160, )))
    self.assertFalse(arena.CheckTerms(start=8, magnitudes=(8, 9)))
    self.assertFalse(arena.CheckTerms(start=16, magnitudes=(1600, 1601)))
    self.assertRaises(ElementBeyondKnownSoughtException,
                      arena.CheckTerms, start=16, magnitudes=(160, 161))

  def test_group_insertion(self):
    arena = PSArena(magnitudes=range(10))

    # Create a group with structure ((5, 6), (7, 8)), and add it to arena.
    gp_56_78 = PSObjectFromStructure( ((5, 6), (7, 8)) )
    gp_56_78.items[0].items[0].DescribeAs(CategoryPrime())
    self.assertFalse(arena.element[5].IsKnownAsInstanceOf(CategoryPrime()))
    # Cannot insert this without spans added... we won't know where it should go.
    self.assertRaises(CannotInsertGroupWithoutSpans, arena.MergeObject, gp_56_78)

    self.assertFalse(arena.GetObjectsWithSpan((5, 8)))

    gp_56_78.SetSpanStart(5)
    inserted_gp = arena.MergeObject(gp_56_78)
    self.assertEqual((5, 8), inserted_gp.Span())

    self.assertEqual(arena.element[5], inserted_gp.items[0].items[0])
    self.assertEqual(arena.element[8], inserted_gp.items[1].items[1])

    self.assertEqual(inserted_gp, arena.GetObjectsWithSpan((5,8))[((5, 6), (7, 8))])
    self.assertEqual(inserted_gp.items[0], arena.GetObjectsWithSpan((5,6))[(5, 6)])
    self.assertEqual(inserted_gp.items[1], arena.GetObjectsWithSpan((7, 8))[(7, 8)])
    self.assertTrue(arena.element[5].IsKnownAsInstanceOf(CategoryPrime()))

    gp_10_11 = PSObjectFromStructure( (10, 11) )
    gp_10_11.SetSpanStart(2)
    self.assertRaises(UnmergableObjectException, arena.MergeObject, gp_10_11)

    gp_11_12 = PSObjectFromStructure( (11, 12) )
    gp_11_12.SetSpanStart(11)
    self.assertRaises(ElementWayBeyondKnownSoughtException, arena.MergeObject, gp_11_12)

    gp_9_10_11 = PSObjectFromStructure( (9, (10, 11)) )
    gp_9_10_11.SetSpanStart(9)
    arena.MergeObject(gp_9_10_11)
    self.assertEqual(12, arena.Size())

  def test_group_insertion_deeper(self):
    """Make sure deeper features of the logic get copied."""

    arena = PSArena(magnitudes=(7, ))
    arena.element[0].DescribeAs(CategoryPrime())

    elt = PSElement(magnitude=7)
    logic = elt.DescribeAs(CategoryPrime())
    inner_logic = logic.Attributes()['index'].DescribeAs(CategoryPrime())
    self.assertEqual(1, inner_logic.Attributes()['index'].magnitude)

    elt.SetSpanStart(0)
    arena.MergeObject(elt)

    self.assertTrue(arena.element[0].IsKnownAsInstanceOf(CategoryPrime()))
    logic = arena.element[0].categories[CategoryPrime()]
    self.assertTrue(logic.Attributes()['index'].IsKnownAsInstanceOf(CategoryPrime()))

