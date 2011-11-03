import unittest
import os
import tempfile

from farg import ltm

class TestLTM(unittest.TestCase):
  def setUp(self):
    filehandle, self.filename = tempfile.mkstemp()

  def tearDown(self):
    # print "Removing %s" % self.filename
    os.remove(self.filename)

  def test_sanity(self):
    myltm = ltm.LTM(self.filename)
    myltm.AddNode(15)
    myltm.AddNode(17)

    myltm.Dump()

    myltm2 = ltm.LTM(self.filename)
    self.assertEqual(2, len(myltm2.nodes))
    self.assertEqual((15, 17), tuple(myltm2.nodes))
