import unittest
from components.stream import Stream

class MyFocusable(object):
  def __init__(self, x):
    self.x = x
    self.y = 2 * x

  def GetFringe(self):
    return { self.x: 0.7, self.y: 0.4 }

class TestStream(unittest.TestCase):
  def test_basic(self):
    s = Stream()
    self.assertEqual(0, s.FociCount())

    m3 = MyFocusable(3)
    m6 = MyFocusable(6)
    m12 = MyFocusable(12)

    hits_map = s.FocusOn(m3)
    self.assertEqual(1, s.FociCount())
    self.assertEqual(0, len(hits_map))

    hits_map = s.FocusOn(m3)
    self.assertEqual(1, s.FociCount())
    self.assertEqual(0, len(hits_map))

    hits_map = s.FocusOn(m6)
    self.assertEqual(2, s.FociCount())
    self.assertEqual(1, len(hits_map))
    self.assertTrue(m3 in hits_map)
    self.assertAlmostEqual(0.28, hits_map[m3])

    hits_map = s.FocusOn(m12)
    self.assertEqual(3, s.FociCount())
    self.assertEqual(1, len(hits_map))
    self.assertTrue(m6 in hits_map)
    self.assertAlmostEqual(0.28, hits_map[m6])

    hits_map = s.FocusOn(m6)
    self.assertEqual(3, s.FociCount())
    self.assertEqual(2, len(hits_map))
    self.assertTrue(m3 in hits_map)
    self.assertTrue(m12 in hits_map)
    self.assertAlmostEqual(0.28, hits_map[m12])
    self.assertAlmostEqual(0.2527, hits_map[m3])
