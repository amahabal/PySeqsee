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
    m1 = NumericMapping(name='succ', category=Prime())
    m2 = NumericMapping(name='succ', category=Prime())
    m3 = NumericMapping(name='pred', category=Prime())
    m4 = NumericMapping(name='succ', category=Number())
    self.assertEqual(m1, m2)
    self.assertNotEqual(m1, m3)
    self.assertNotEqual(m1, m4)
    self.assertNotEqual(m3, m4)

    # Also test this with parametrized categories.
    for content in (m1, m2, m3, m4):
      myltm.GetNodeForContent(content)
    myltm.Dump()

    # Let's clear the memos for NumericMapping.
    NumericMapping.__memo__.clear()

    myltm2 = LTMGraph(self.filename)
    self.assertEqual(5, len(myltm2.nodes))
    m1_like_node = NumericMapping(name='succ', category=Prime())
    self.assertNotEqual(m1_like_node, m1)
    self.assertNotEqual(m1_like_node.GetLTMStorableContent(), m1.GetLTMStorableContent())
    myltm2.GetNodeForContent(m1_like_node)
    self.assertEqual(5, len(myltm2.nodes))
