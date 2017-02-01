import unittest
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
    self.assertFalse(e1.is_anchored)

    g1 = PSGroup(items=(e1, e2))
    self.assertIsInstance(g1, PSGroup)
    self.assertIsInstance(g1, PSObject)

    self.assertEqual((3,3), g1.Structure())
    self.assertEqual("(3, 3)", g1.GetStorable().rep)
