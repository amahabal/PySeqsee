import unittest
import os
import tempfile

from farg import ltm

class MockCategory(ltm.LTMStorableMixin):
  def __init__(self, foo):
    print "Initializing MockCategory instance ", self
    self.foo = foo

class MockMapping(ltm.LTMStorableMixin):
  def __init__(self, category):
    self.category = category


class TestLTMNode(unittest.TestCase):
  def test_sanity(self):
    node = ltm.LTMNode(MockCategory.Create(foo=3))
    self.assertEqual(MockCategory.Create(foo=3), node.content)

class TestLTM(unittest.TestCase):
  def setUp(self):
    filehandle, self.nodes_filename = tempfile.mkstemp()
    filehandle, self.edges_filename = tempfile.mkstemp()

  def tearDown(self):
    os.remove(self.nodes_filename)
    os.remove(self.edges_filename)

  def test_sanity(self):
    myltm = ltm.LTM(self.nodes_filename, self.edges_filename)
    c1 = MockCategory.Create(foo=7)
    m1 = MockMapping.Create(category=c1)
    c2 = MockCategory.Create(foo=9)
    m2 = MockMapping.Create(category=c2)

    myltm.AddNode(ltm.LTMNode(c1))
    myltm.AddNode(ltm.LTMNode(m1))
    myltm.AddNode(ltm.LTMNode(c2))
    myltm.AddNode(ltm.LTMNode(m2))

    myltm.Dump()

    # I'll remove the memos for MockMapping but not MockCategory, thereby testing the creation
    # mechanism.
    MockMapping.memos = {}
    # MockCategory.memos = {}

    myltm2 = ltm.LTM(self.nodes_filename, self.edges_filename)
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

    myltm = ltm.LTM(self.nodes_filename, self.edges_filename)
    c1 = MockCategory.Create(foo=7)
    m1 = MockMapping.Create(category=c1)
    c2 = MockCategory.Create(foo=9)
    m2 = MockMapping.Create(category=c2)

    # Add in a strange order...
    myltm.AddNode(ltm.LTMNode(m1))
    myltm.AddNode(ltm.LTMNode(m2))
    myltm.AddNode(ltm.LTMNode(c1))
    myltm.AddNode(ltm.LTMNode(c2))

    myltm.Dump()

    MockMapping.memos = {}

    myltm2 = ltm.LTM(self.nodes_filename, self.edges_filename)
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

    myltm = ltm.LTM(self.nodes_filename, self.edges_filename)
    c1 = MockCategory.Create(foo=7)
    m1 = MockMapping.Create(category=c1)
    c2 = MockCategory.Create(foo=9)
    m2 = MockMapping.Create(category=c2)

    myltm.AddNode(ltm.LTMNode(m1))
    myltm.AddNode(ltm.LTMNode(m2))
    myltm.AddNode(ltm.LTMNode(c1))
    myltm.AddNode(ltm.LTMNode(c2))

    myltm.AddEdge(m1, c1)
    edges = myltm.GetNode(m1).GetOutgoingEdges()
    self.assertEqual(c1, edges[0].to_node.content)
    self.assertEqual(ltm.LTM_EDGE_TYPE_RELATED, edges[0].edge_type)
