import unittest
from farg.apps.pyseqsee.arena import PSArena, ElementBeyondKnownSoughtException
from farg.apps.pyseqsee.objects import PSGroup, PSElement


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
