"""Utilities for testing."""
from farg.apps.pyseqsee.utils import PSObjectFromStructure

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

def CategoryLogicTester(*, test, item, cat, tester):
  """Describes item as cat, and checks that logic passes the checks posed by tester.

  tester is a function that takes the test and logic as the arguments."""
  logic = item.DescribeAs(cat)
  tester(test, logic)

def StructureTester(**structure_dict):
  """Creates a logic tester that checks that the structure of attributes in logic."""
  def tester(test, logic):
    attributes = logic.Attributes()
    for k, v in structure_dict.items():
      test.assertEqual(v, attributes[k].Structure())
  return tester

def FringeTest(*, test, item, expected_fringe_parts):
  """What parts to expect in item.GetFringe()?"""
  test.assertEqual(sorted(repr(x) for x in expected_fringe_parts),
                   sorted(repr(x) for x in item.GetFringe().keys()))
