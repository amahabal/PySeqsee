from farg.ltm.edge import LTMEdge
from farg.ltm.graph import LTMGraph
from farg.ltm.node import LTMNode
from farg.ltm.storable import LTMStorableMixin
from apps.seqsee.mapping import NumericMapping, StructuralMapping
from apps.seqsee.categories import Number, Prime
import os
import tempfile
import unittest

class LTMTestBase(unittest.TestCase):
  def setUp(self):
    filehandle, self.filename = tempfile.mkstemp()

  def tearDown(self):
    os.remove(self.filename)

class TestLTMWithMappings(LTMTestBase):
  def test_sanity(self):
    myltm = LTMGraph(self.filename)
    m1 = NumericMapping(name='succ', category=Prime)
    m2 = NumericMapping(name='succ', category=Prime)
    m3 = NumericMapping(name='pred', category=Prime)
    m4 = NumericMapping(name='succ', category=Number)
    self.assertEqual(m1, m2)
    self.assertNotEqual(m1, m3)
    self.assertNotEqual(m1, m4)
    self.assertNotEqual(m3, m4)

    # Also test this with parametrized categories.
    for content in (m1, m2, m3, m4):
      myltm.GetNodeForContent(content)
    myltm.Dump()

    myltm2 = LTMGraph(self.filename)
    self.assertEqual(3, len(myltm2.nodes))
    self.assertEqual(myltm2.GetNodeForContent(m1),
                     myltm2.GetNodeForContent(NumericMapping(name='succ',
                                                             category=Prime)))
