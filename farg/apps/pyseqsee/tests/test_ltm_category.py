"""Tests putting categories into an LTM and pulling them out to test their ability to thaw."""

import os
import tempfile
import unittest

from farg.core.ltm.graph import LTMGraph
from farg.apps.pyseqsee.categorization.numeric import CategoryEvenInteger, CategoryPrime
from farg.apps.pyseqsee.categorization import categories as C

class LTMTestBase(unittest.TestCase):

  def tearDown(self):
    os.remove(self.filename)

  def assert_dump_and_revive(self, *, nodecount, class_name, arguments_creator=None,
                             classes_to_clear=None):
    """This method tests inserting an item in a graph, and testing it post-revival.

    Adding a node can add other nodes dependent on it. nodecount contains the count to expect.
    To create the item to insert, we provide a class nae and arguments, but arguments are provided
    as a lambda which, when run, provides a dictionary. These shenanigans are necessary to get
    around memoization: between graph creation and its revival, we clear the memoization cache of
    the relevant classes (provided via classes_to_clear).

    Finally, after the graph has been revived, we insert the "same" object again and ensure that the
    node count does not go up, thereby showing that the node was already present.
    """
    unused_filehandle, self.filename = tempfile.mkstemp()
    graph = LTMGraph(filename=self.filename)
    kwargs = dict()
    if arguments_creator:
      kwargs = arguments_creator()
    graph.GetNode(content=class_name(**kwargs))
    graph.DumpToFile()

    if classes_to_clear:
      for c in classes_to_clear:
        c.__memo__.clear()

    graph2 = LTMGraph(filename=self.filename)
    node_count_before = len(graph2.GetNodes())
    self.assertEqual(nodecount, node_count_before)
    kwargs = dict()
    if arguments_creator:
      kwargs = arguments_creator()
    graph2.GetNode(content=class_name(**kwargs))
    self.assertEqual(len(graph2.GetNodes()), node_count_before, "Node existed")


  def test_argumentless_categories(self):
    self.assert_dump_and_revive(class_name=CategoryEvenInteger, nodecount=1)
    self.assert_dump_and_revive(class_name=C.CategoryAnyObject, nodecount=1)
    self.assert_dump_and_revive(class_name=CategoryPrime, nodecount=1)

  def test_multipart(self):
    classes_to_clear = (CategoryEvenInteger, C.CategoryAnyObject, C.MultiPartCategory)
    def arguments_creator():
      return dict(parts_count=2,
                  part_categories=(CategoryEvenInteger(),
                                   C.CategoryAnyObject()))
    self.assert_dump_and_revive(class_name=C.MultiPartCategory,
                                nodecount=3, # This, plus Even and AnyObject
                                arguments_creator=arguments_creator,
                                classes_to_clear=classes_to_clear)

  def test_compound(self):
    classes_to_clear = (C.BasicSuccessorCategory, C.RepeatedIntegerCategory, C.CompoundCategory)
    def arguments_creator():
      return dict(base_category=C.BasicSuccessorCategory(),
                  attribute_categories=(('end', C.BasicSuccessorCategory()),
                                        ('length', C.BasicSuccessorCategory()),
                                        ('start', C.RepeatedIntegerCategory())))
    self.assert_dump_and_revive(class_name=C.CompoundCategory,
                                nodecount=3, # This, plus successor and repeated
                                arguments_creator=arguments_creator,
                                classes_to_clear=classes_to_clear)
