import unittest
import os
import tempfile

from farg.core.ltm.edge import LTMEdge
from farg.core.ltm.graph import LTMGraph
from farg.core.ltm.node import LTMNode
from farg.core.ltm.storable import LTMStorableMixin

from farg.apps.seqsee.sobject import SObject, SElement, SGroup, LTMStorableSObject
from farg.apps.seqsee.anchored import SAnchored

class LTMTestBase(unittest.TestCase):
  def setUp(self):
    unused_filehandle, self.filename = tempfile.mkstemp()

  def tearDown(self):
    os.remove(self.filename)

class TestLTMWithObjects(LTMTestBase):
  def test_sanity(self):
    myltm = LTMGraph(self.filename)
    o1 = SObject.Create([1])
    o1b = SObject.Create([1])
    o2 = SObject.Create([2])
    o12 = SObject.Create([1, 2])
    o123 = SObject.Create([1, 2, 3])
    o1_23 = SObject.Create([1, (2, 3)])

    self.assertNotEqual(o1, o1b)
    self.assertEqual(o1.GetLTMStorableContent(), o1b.GetLTMStorableContent())
    self.assertEqual(myltm.GetNode(content=o1), myltm.GetNode(content=o1b))

    for content in (o1, o1b, o2, o12, o123, o1_23):
      myltm.GetNode(content=content)

    self.assertEqual(myltm.GetNode(content=o1),
                     myltm.GetNode(content=SAnchored(o1, None, 5, 5)))

    self.assertEqual(myltm.GetNode(content=SAnchored(o1b, None, 6, 6)),
                     myltm.GetNode(content=SAnchored(o1, None, 5, 5)))

    self.assertNotEqual(myltm.GetNode(content=SAnchored(o1b, None, 6, 6)),
                        myltm.GetNode(content=SAnchored(o1_23, None, 5, 7)))

    node = myltm.GetNode(content=SAnchored(o1_23, None, 5, 7))
    self.assertEqual(LTMStorableSObject, node.content.__class__)
    self.assertEqual((1, (2, 3)), node.content.structure)

    myltm.Dump()

    myltm2 = LTMGraph(self.filename)
    self.assertEqual(5, len(myltm2.nodes))
