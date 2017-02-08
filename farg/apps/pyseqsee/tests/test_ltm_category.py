"""Tests putting categories into an LTM and pulling them out to test their ability to thaw."""

import os
import tempfile
import unittest

from farg.core.ltm.graph import LTMGraph
from farg.apps.pyseqsee.categorization.numeric import CategoryEvenInteger, CategoryPrime
from farg.apps.pyseqsee.categorization import categories as C
from farg.apps.pyseqsee.objects import PSElement, PSGroup

def PSObjectFromStructure(structure):
  if isinstance(structure, int):
    return PSElement(magnitude=structure)
  assert(isinstance(structure, tuple))
  parts = [PSObjectFromStructure(x) for x in structure]
  return PSGroup(items=parts)

def CategoryTester(*, positive, negative):
  """Given two lists of structures, returns a 2-argument function (with a category as the second arg)
     that tests each of these structures for the category.
  """
  def Tester(test, category):
    for p in positive:
      obj = PSObjectFromStructure(p)
      test.assertTrue(obj.DescribeAs(category), "Describing %s as %s" % (obj.Structure(),
                                                                         category.BriefLabel()))
    for n in negative:
      obj = PSObjectFromStructure(n)
      test.assertFalse(obj.DescribeAs(category), "Describing %s as %s" % (obj.Structure(),
                                                                          category.BriefLabel()))
  return Tester

class LTMTestBase(unittest.TestCase):

  def tearDown(self):
    os.remove(self.filename)

  def assert_dump_and_revive(self, *, nodecount, class_name, arguments_creator=None,
                             classes_to_clear=None, extra_tests=None):
    """This method tests inserting an item in a graph, and testing it post-revival.

    Adding a node can add other nodes dependent on it. nodecount contains the count to expect.
    To create the item to insert, we provide a class nae and arguments, but arguments are provided
    as a lambda which, when run, provides a dictionary. These shenanigans are necessary to get
    around memoization: between graph creation and its revival, we clear the memoization cache of
    the relevant classes (provided via classes_to_clear).

    Finally, after the graph has been revived, we insert the "same" object again and ensure that the
    node count does not go up, thereby showing that the node was already present.

    Finally, if extra_tests is passed in, it must be a function taking two arguments: self (for the
    test class) and cat (the constructed category), and it can run whatever tests it sees fit.
    """
    unused_filehandle, self.filename = tempfile.mkstemp()
    graph = LTMGraph(filename=self.filename)
    kwargs = dict()
    if arguments_creator:
      kwargs = arguments_creator()
    cat = class_name(**kwargs)
    graph.GetNode(content=cat)

    if extra_tests:
      extra_tests(self, cat)

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
    cat = class_name(**kwargs)
    if extra_tests:
      extra_tests(self, cat)


    graph2.GetNode(content=cat)
    self.assertEqual(len(graph2.GetNodes()), node_count_before, "Node existed")


  def test_argumentless_categories(self):
    self.assert_dump_and_revive(
      class_name=CategoryEvenInteger, nodecount=1,
      extra_tests=CategoryTester(positive=(4,
                                           6),
                                 negative=(3,
                                           (),
                                           (2, 4))))
    self.assert_dump_and_revive(
      class_name=C.CategoryAnyObject, nodecount=1,
      extra_tests=CategoryTester(positive=(4,
                                           (4, 6),
                                           ()),
                                 negative=()))
    self.assert_dump_and_revive(
      class_name=CategoryPrime, nodecount=1,
      extra_tests=CategoryTester(positive=(3,
                                           7),
                                 negative=(9,
                                           0,
                                           (3,),
                                           ())))

  def test_multipart(self):
    classes_to_clear = (CategoryEvenInteger, C.CategoryAnyObject, C.MultiPartCategory)
    def arguments_creator():
      return dict(parts_count=2,
                  part_categories=(CategoryEvenInteger(),
                                   C.CategoryAnyObject()))
    self.assert_dump_and_revive(
      class_name=C.MultiPartCategory,
      nodecount=3, # This, plus Even and AnyObject
      arguments_creator=arguments_creator,
      classes_to_clear=classes_to_clear,
      extra_tests=CategoryTester(positive=( (8, ()),
                                            (6, 9),
                                            (2, (2, 3, (4, 5)))),
                                 negative=( (7, 8),
                                            (6, 8, 9),
                                            ())))

  def test_compound(self):
    classes_to_clear = (C.BasicSuccessorCategory, C.RepeatedIntegerCategory, C.CompoundCategory)
    def arguments_creator():
      return dict(base_category=C.BasicSuccessorCategory(),
                  attribute_categories=(('end', C.BasicSuccessorCategory()),
                                        ('length', C.BasicSuccessorCategory()),
                                        ('start', C.RepeatedIntegerCategory())))
    self.assert_dump_and_revive(
      class_name=C.CompoundCategory,
      nodecount=3, # This, plus successor and repeated
      arguments_creator=arguments_creator,
      classes_to_clear=classes_to_clear,
      extra_tests=CategoryTester(positive=( ((5, 6), (5, 6, 7)),
                                            ((5, 6), ),
                                            ((5, 6, 7), (5, 6, 7, 8), (5, 6, 7, 8, 9)),
                                            ()),
                                 negative=( ((6, 5), (6, 5, 4)),
                                            ((6, 5),))))
