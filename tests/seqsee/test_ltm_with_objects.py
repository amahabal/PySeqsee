import unittest
import os
import tempfile

from farg.ltm.edge import LTMEdge
from farg.ltm.graph import LTMGraph
from farg.ltm.node import LTMNode
from farg.ltm.storable import LTMStorableMixin

from apps.seqsee.sobject import SObject, SElement, SGroup
from apps.seqsee.anchored import SAnchored

class LTMTestBase(unittest.TestCase):
  def setUp(self):
    filehandle, self.filename = tempfile.mkstemp()

  def tearDown(self):
    os.remove(self.filename)

class TestLTMWithObjects(LTMTestBase):
  def test_sanity(self):
    myltm = LTMGraph(self.filename)
    o1 = SObject.Create(1)
    o1b = SObject.Create(1)
    o2 = SObject.Create(2)
    o12 = SObject.Create(1, 2)
    o123 = SObject.Create(1, 2, 3)
    o1_23 = SObject.Create(1, (2, 3))

    self.assertNotEqual(o1, o1b)
    self.assertEqual(o1.GetStorable(), o1b.GetStorable())
    self.assertEqual(myltm.GetNodeForContent(o1), myltm.GetNodeForContent(o1b))

    for content in (o1, o1b, o2, o12, o123, o1_23):
      myltm.GetNodeForContent(content)

    self.assertNotEqual(myltm.GetNodeForContent(o1),
                        myltm.GetNodeForContent(SAnchored(o1, None, 5, 5)))

    self.assertEqual(myltm.GetNodeForContent(SAnchored(o1b, None, 6, 6)),
                     myltm.GetNodeForContent(SAnchored(o1, None, 5, 5)))

    self.assertNotEqual(myltm.GetNodeForContent(SAnchored(o1b, None, 6, 6)),
                        myltm.GetNodeForContent(SAnchored(o1_23, None, 5, 7)))

    node = myltm.GetNodeForContent(SAnchored(o1_23, None, 5, 7))
    self.assertEqual(SAnchored, node.content.cls)
    self.assertEqual((1, (2, 3)), node.content.storable)

    myltm.Dump()

    myltm2 = LTMGraph(self.filename)
    self.assertEqual(7, len(myltm2._nodes))
