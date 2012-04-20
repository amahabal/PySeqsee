from farg.apps.seqsee.anchored import SAnchored, NonAdjacentGroupElementsException
from farg.apps.seqsee.sobject import SObject
from farg.core.exceptions import FargError
import unittest

class TestSObject(unittest.TestCase):
  def test_object_creation(self):
    o1 = SObject.Create(3)
    self.assertTrue(isinstance(o1, SObject))
    self.assertFalse(o1.is_group)

    o1a = SObject.Create([3])
    self.assertTrue(isinstance(o1a, SObject))
    self.assertFalse(o1a.is_group)

    o2 = SObject.Create(3, 4)
    self.assertTrue(isinstance(o2, SObject))
    self.assertTrue(o2.is_group)
    self.assertEqual(4, o2.items[1].magnitude)

    o2a = SObject.Create([3, 4])
    self.assertTrue(isinstance(o2a, SObject))
    self.assertTrue(o2a.is_group)
    self.assertEqual(4, o2a.items[1].magnitude)

    o2b = SObject.Create(o2)
    self.assertTrue(isinstance(o2b, SObject))
    self.assertTrue(o2b.is_group)
    self.assertEqual(4, o2b.items[1].magnitude)

  def test_anchored_creation(self):
    o1 = SObject.Create(3)
    o1_anc = SAnchored(o1, [], 3, 3)

    o2 = SObject.Create(40)
    o2_anc = SAnchored(o2, [], 4, 4)

    o3 = SObject.Create(30)
    o3_anc = SAnchored(o3, [], 5, 5)

    # Create expects anchored objects...
    self.assertRaises(FargError, SAnchored.Create, o1)

    # With a single arg, the object is returned unchanged.
    self.assertEqual(o1_anc, SAnchored.Create(o1_anc))

    # With multiple args, we expect the positions of these to be adjacent.
    self.assertRaises(NonAdjacentGroupElementsException,
                      SAnchored.Create, o1_anc, o3_anc)

    # This also implies that elements may not be repeated:
    self.assertRaises(NonAdjacentGroupElementsException,
                      SAnchored.Create, o1_anc, o1_anc)

    # If ranges are fine, the group is constructed fine:
    o123_anc = SAnchored.Create(o1_anc, o2_anc, o3_anc)
    self.assertEqual((3, 5), o123_anc.Span())
    self.assertEqual((3, 40, 30), o123_anc.Structure())


  def test_position(self):
    o2a = SObject.Create([3, 4])
    o2a_anchored = SAnchored(o2a, [], 10, 12)
    self.assertEqual(10, o2a_anchored.start_pos)
