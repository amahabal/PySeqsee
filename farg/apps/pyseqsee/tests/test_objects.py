import unittest

from farg.apps.pyseqsee.arena import PSArena
from farg.apps.pyseqsee.objects import PlatonicObject, PSElement, PSGroup, PSObject
from farg.core.ltm.storable import LTMNodeContent


class TestPlatonicObject(unittest.TestCase):
  """Tests creation and uniqueness of platonic objects."""

  def test_creation(self):

    # Constructor only takes strings.
    self.assertRaises(AssertionError, PlatonicObject, rep=3)

    p1 = PlatonicObject(rep="3")
    self.assertIsInstance(p1, LTMNodeContent)
    self.assertEqual("3", p1.rep)

    p2 = PlatonicObject(rep="3")
    self.assertEqual(p1, p2, "Same object when same args")

  def test_factory(self):
    # Must be passed in an int or a tuple.
    self.assertRaises(AssertionError, PlatonicObject.CreateFromStructure, "3")
    self.assertRaises(AssertionError, PlatonicObject.CreateFromStructure, [3])

    p1 = PlatonicObject.CreateFromStructure(3)
    self.assertEqual("3", p1.rep)
    p2 = PlatonicObject.CreateFromStructure(3)
    self.assertEqual(p1, p2, "Same object when same args")

    p3 = PlatonicObject.CreateFromStructure((3, 4))
    self.assertEqual("(3, 4)", p3.rep)
    p4 = PlatonicObject.CreateFromStructure((3, 4))
    self.assertEqual(p3, p4, "Same object when same args")

    p5 = PlatonicObject.CreateFromStructure((3,))
    self.assertEqual("(3)", p5.rep)

    p6 = PlatonicObject.CreateFromStructure((3, ((4, 5),)))
    self.assertEqual("(3, ((4, 5)))", p6.rep)


class TestPSObject(unittest.TestCase):

  def test_creation(self):
    # PSElement can be created by passing in magnitude.
    e1 = PSElement(magnitude=3)
    self.assertIsInstance(e1, PSElement)
    self.assertIsInstance(e1, PSObject)
    self.assertEqual(3, e1.magnitude)

    # It is not memoized.
    e2 = PSElement(magnitude=3)
    self.assertNotEqual(e1, e2)

    # It is not anchored.
    self.assertIsNone(e1.Span())

    g1 = PSGroup(items=(e1, e2))
    self.assertIsInstance(g1, PSGroup)
    self.assertIsInstance(g1, PSObject)

    self.assertEqual((3, 3), g1.Structure())
    self.assertEqual("(3, 3)", g1.GetLTMStorableContent().rep)

    g_empty = PSGroup(items=())
    self.assertIsInstance(g_empty, PSGroup)
    self.assertEqual("()", g_empty.GetLTMStorableContent().rep)

    g_deeply_empty = PSGroup(items=(g_empty,))
    self.assertIsInstance(g_deeply_empty, PSGroup)
    self.assertEqual("(())", g_deeply_empty.GetLTMStorableContent().rep)

  def test_offsets(self):
    elements = [PSElement(magnitude=x) for x in range(10)]

    g36 = PSGroup(items=elements[3:7])
    g12 = PSGroup(items=elements[1:3])
    g_12_36 = PSGroup(items=(g12, g36))

    # We will attach a start offset to this large group. It will cause its pieces to get offsets,
    # too.
    g_12_36.SetSpanStart(1)
    self.assertEqual((1, 6), g_12_36.Span())
    self.assertEqual((1, 2), g12.Span())
    self.assertEqual((3, 6), g36.Span())
    self.assertEqual((6, 6), elements[6].Span())
    self.assertIsNone(elements[0].Span())

    # What if we try to set existing span? It is okay if the new value is the same as the old, else
    # it is an assert error.
    g36.SetSpanStart(3)  # Not a problem.
    elements[5].SetSpanStart(5)  # Not a problem.
    self.assertRaises(AssertionError, elements[5].SetSpanStart, 2)
    self.assertRaises(AssertionError, g36.SetSpanStart, 2)

    g_0_16 = PSGroup(items=[elements[0], g_12_36])
    # We cannot set the start value to be from 7...
    self.assertRaises(AssertionError, g_0_16.SetSpanStart, 7)
    # Note that setting spans is all or nothings: we don't want to have set the span of 0 in the
    # process.
    self.assertIsNone(elements[0].Span())

    # We should also be able to infer spans if some piece has the span set...
    self.assertTrue(g_0_16.InferSpans())
    self.assertEqual((0, 0), elements[0].Span())

    # Of course, it is possible that no consistent assignment is possible. In that case, we should
    # bail, without setting *any* offsets.
    elements[9].SetSpanStart(9)
    # This group will have a bogus span...
    g_06_89 = PSGroup(items=(g_0_16, elements[8], elements[9]))
    self.assertFalse(g_06_89.InferSpans())
    self.assertIsNone(elements[8].Span())

  def test_offsets_with_empty(self):
    elements = [PSElement(magnitude=x) for x in range(10)]

    g_empty = PSGroup(items=())
    g36 = PSGroup(items=elements[3:7])
    g12 = PSGroup(items=elements[1:3])
    g_12_36 = PSGroup(items=(g12, g_empty, g36))
    g_12_36.SetSpanStart(1)

    self.assertEqual((1, 6), g_12_36.Span())
    self.assertEqual((1, 2), g12.Span())
    self.assertEqual((3, 6), g36.Span())
    self.assertEqual((6, 6), elements[6].Span())
    self.assertEqual((3, 2), g_empty.Span())

  def test_hypothetical_insert(self):
    arena = PSArena(magnitudes=range(10), start=5)
    gp = PSGroup(items=arena.element[2:5])
    self.assertTrue(gp.InferSpans())
    self.assertEqual((7, 9), gp.Span())

    gp2 = gp.HypotheticallyAddComponentBefore(arena.element[1])
    self.assertEqual((7, 9), gp.Span())
    self.assertEqual((2, 3, 4), gp.Structure())
    self.assertEqual((6, 9), gp2.Span())
    self.assertEqual((1, 2, 3, 4), gp2.Structure())

    gp3 = gp2.HypotheticallyAddComponentAfter(arena.element[5])
    self.assertEqual((6, 10), gp3.Span())
    self.assertEqual((1, 2, 3, 4, 5), gp3.Structure())
