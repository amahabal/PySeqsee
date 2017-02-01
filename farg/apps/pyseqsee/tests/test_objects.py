import unittest
from farg.apps.pyseqsee.objects import PlatonicObject
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
