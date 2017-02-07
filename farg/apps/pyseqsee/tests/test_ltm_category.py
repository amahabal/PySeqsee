"""Tests putting categories into an LTM and pulling them out to test their ability to thaw."""

import os
import tempfile
import unittest

from farg.core.ltm.graph import LTMGraph
from farg.apps.pyseqsee.categorization.numeric import CategoryEvenInteger
from farg.apps.pyseqsee.categorization import categories as C

class LTMTestBase(unittest.TestCase):

  def tearDown(self):
    os.remove(self.filename)

  def assert_dump_and_revive(self, *, class_name, nodecount, **kwargs):
    unused_filehandle, self.filename = tempfile.mkstemp()
    graph = LTMGraph(filename=self.filename)
    graph.GetNode(content=class_name(**kwargs))
    graph.DumpToFile()

    graph2 = LTMGraph(filename=self.filename)
    node_count_before = len(graph2.GetNodes())
    self.assertEqual(nodecount, node_count_before)
    graph2.GetNode(content=class_name(**kwargs))
    self.assertEqual(len(graph2.GetNodes()), node_count_before, "Node existed")


  def test_argumentless_categories(self):
    self.assert_dump_and_revive(class_name=CategoryEvenInteger, nodecount=1)
    self.assert_dump_and_revive(class_name=C.CategoryAnyObject, nodecount=1)
    
