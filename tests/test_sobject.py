import unittest
from apps.seqsee.sobject import SAnchored, SObject

class TestSObject(unittest.TestCase):
  def test_creation(self):
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

  def test_position(self):
    o2a = SObject.Create([3, 4])
    o2a_anchored = SAnchored(o2a, 10, 12)
    self.assertEqual(10, o2a_anchored.start_pos)
