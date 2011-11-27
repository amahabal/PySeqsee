import unittest
import os
import tempfile

from farg import ltm_old
from farg.ltm.edge import LTMEdge
from farg.ltm.graph import LTMGraph
from farg.ltm.node import LTMNode

class MockCategory(ltm_old.LTMStorableMixin):
  def __init__(self, foo):
    print "Initializing MockCategory instance ", self
    self.foo = foo

class MockMapping(ltm_old.LTMStorableMixin):
  def __init__(self, category):
    self.category = category


class TestLTMNode(unittest.TestCase):
  def test_sanity(self):
    node = LTMNode(MockCategory.Create(foo=3))
    self.assertEqual(MockCategory.Create(foo=3), node.content)

class LTMTestBase(unittest.TestCase):
  def setUp(self):
    filehandle, self.filename = tempfile.mkstemp()

  def tearDown(self):
    os.remove(self.filename)

class TestLTM(LTMTestBase):
  def test_sanity(self):
    myltm = LTMGraph(self.filename)
    c1 = MockCategory.Create(foo=7)
    m1 = MockMapping.Create(category=c1)
    c2 = MockCategory.Create(foo=9)
    m2 = MockMapping.Create(category=c2)

    for content in (c1, m1, c2, m2):
      myltm.GetNodeForContent(content)

    myltm.Dump()

    # I'll remove the memos for MockMapping but not MockCategory, thereby testing the creation
    # mechanism.
    MockMapping.memos = {}
    # MockCategory.memos = {}

    myltm2 = LTMGraph(self.filename)
    self.assertEqual(4, len(myltm2.nodes))
    c1p, m1p, c2p, m2p = (x.content for x in myltm2.nodes)
    self.assertEqual(7, c1p.foo)
    self.assertEqual(9, c2p.foo)
    self.assertEqual(c1p, m1p.category)
    self.assertEqual(c2p, m2p.category)

    c3 = MockCategory.Create(foo=9)
    self.assertEqual(c3, c2p)

    m3 = MockMapping.Create(category=c3)
    self.assertEqual(m3, m2p)

  def test_dependencies_are_after_nodes(self):
    MockMapping.memos = {}
    MockCategory.memos = {}

    myltm = LTMGraph(self.filename)
    c1 = MockCategory.Create(foo=7)
    m1 = MockMapping.Create(category=c1)
    c2 = MockCategory.Create(foo=9)
    m2 = MockMapping.Create(category=c2)

    # Add in a strange order...
    for content in (m1, m2, c1, c2):
      myltm.GetNodeForContent(content)

    myltm.Dump()

    MockMapping.memos = {}

    myltm2 = LTMGraph(self.filename)
    self.assertEqual(4, len(myltm2.nodes))
    m1p, m2p, c1p, c2p = (x.content for x in myltm2.nodes)

    self.assertEqual(7, c1p.foo)
    self.assertEqual(9, c2p.foo)
    self.assertEqual(c1p, m1p.category)
    self.assertEqual(c2p, m2p.category)

    c3 = MockCategory.Create(foo=9)
    self.assertEqual(c3, c2p)

    m3 = MockMapping.Create(category=c3)
    self.assertEqual(m3, m2p)

  def test_store_edges(self):
    MockMapping.memos = {}
    MockCategory.memos = {}

    myltm = LTMGraph(self.filename)
    c1 = MockCategory.Create(foo=7)
    m1 = MockMapping.Create(category=c1)
    c2 = MockCategory.Create(foo=9)
    m2 = MockMapping.Create(category=c2)

    for content in (m1, m2, c1, c2):
      myltm.GetNodeForContent(content)

    myltm.AddEdgeBetweenContent(m1, c1)
    edges = myltm.GetNodeForContent(m1).GetOutgoingEdges()
    self.assertEqual(c1, edges[0].to_node.content)
    self.assertEqual(LTMEdge.LTM_EDGE_TYPE_RELATED, edges[0].edge_type)

    myltm.Dump()

    MockMapping.memos = {}
    MockCategory.memos = {}

    myltm2 = LTMGraph(self.filename)
    self.assertEqual(4, len(myltm2.nodes))
    m1p, m2p, c1p, c2p = (x.content for x in myltm2.nodes)
    edges = myltm2.GetNodeForContent(m1p).GetOutgoingEdges()
    self.assertEqual(c1p, edges[0].to_node.content)
    self.assertEqual(LTMEdge.LTM_EDGE_TYPE_RELATED, edges[0].edge_type)

class TestLTM2(LTMTestBase):
  def test_activation(self):
    ltm_old.LTMStorableMixin.ClearMemos()

    myltm = LTMGraph(self.filename)
    c1 = MockCategory.Create(foo=7)
    m1 = MockMapping.Create(category=c1)
    for content in (m1, c1):
      myltm.GetNodeForContent(content)
    myltm.AddEdgeBetweenContent(m1, c1)

    node_m1 = myltm.GetNodeForContent(m1)
    node_c1 = myltm.GetNodeForContent(c1)
    self.assertEqual(0, node_m1.GetRawActivation(current_time=0))
    self.assertEqual(0, node_c1.GetRawActivation(current_time=0))

    # Spiking c1 does not send activation back to m1 (edge is unidirectional).
    node_c1.Spike(10, current_time=0)
    self.assertEqual(0, node_m1.GetRawActivation(current_time=0))
    self.assertEqual(2, node_c1.GetRawActivation(current_time=0))

    # Spiking m1, though, sends activation to c1 as well.
    node_m1.Spike(10, current_time=0)
    self.assertEqual(2, node_m1.GetRawActivation(current_time=0))
    self.assertTrue(2 < node_c1.GetRawActivation(current_time=0))

    self.assertAlmostEqual(0.2, node_c1.depth_reciprocal)
    node_c1.IncrementDepth()
    self.assertAlmostEqual(0.16666666666, node_c1.depth_reciprocal)

    myltm.Dump()
    ltm_old.LTMStorableMixin.ClearMemos()
    myltm2 = LTMGraph(self.filename)
    node_m1p, node_c1p = myltm2.nodes
    m1p, c1p = (x.content for x in myltm2.nodes)
    edges = myltm2.GetNodeForContent(m1p).GetOutgoingEdges()
    self.assertEqual(c1p, edges[0].to_node.content)

    #: Activations reset on loading...
    self.assertEqual(0, node_m1p.GetRawActivation(current_time=0))
    self.assertEqual(0, node_c1p.GetRawActivation(current_time=0))

    #: But depths are maintained.
    self.assertAlmostEqual(0.2, node_m1p.depth_reciprocal)
    self.assertAlmostEqual(0.166666666, node_c1p.depth_reciprocal)
