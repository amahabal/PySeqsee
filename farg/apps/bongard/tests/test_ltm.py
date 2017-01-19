import unittest
import os
import tempfile
from farg.apps.bongard.workspace import PlatonicInteger, IntegerObject
from farg.core.ltm.graph import LTMGraph

class LTMTest(unittest.TestCase):
  def setUp(self):
    unused_filehandle, self.filename = tempfile.mkstemp()

  def tearDown(self):
    os.remove(self.filename)

  def test_storing_integers(self):
    # Create the graph.
    myltm = LTMGraph(self.filename)
    
    # Create nodes that we may want to add.
    pi7 = PlatonicInteger(7)
    # Repeated constructor calls return the same thing.
    self.assertEqual(pi7, PlatonicInteger(7))

    i7 = IntegerObject(7)
    # Let's add nodes to this.
    node = myltm.GetNode(content=i7)
    self.assertEqual(PlatonicInteger, node.content.__class__)
    self.assertEqual(7, node.content.magnitude)
    
    myltm.Dump()

    myltm2 = LTMGraph(self.filename)
    self.assertEqual(1, len(myltm2.nodes))
    node = myltm2.nodes[0]
    self.assertEqual(PlatonicInteger, node.content.__class__)
    self.assertEqual(7, node.content.magnitude)
