from apps.seqsee.categories import Ascending
from apps.seqsee.get_mapping import SubspaceFindMapping
from apps.seqsee.mapping import StructuralMapping
from apps.seqsee.sobject import SObject
from farg.controller import Controller
import unittest


class TestSubspace(unittest.TestCase):
  def test_sanity(self):
    # This test refers to things in the Seqsee app. Maybe the test should move there.
    a3 = SObject.Create(1, 2, 3)
    a4 = SObject.Create(1, 2, 3, 4)
    a5 = SObject.Create(1, 2, 3, 4, 5)

    a19_21 = SObject.Create(19, 20, 21)

    controller = Controller()
    mapping = SubspaceFindMapping(controller, 3, left=a3, right=a4, category=Ascending())
    self.assertTrue(isinstance(mapping, StructuralMapping))
    self.assertEqual(Ascending(), mapping.category)
    self.assertEqual(None, mapping.slippages)

    mapping = SubspaceFindMapping(controller, 3, left=a5, right=a19_21, category=Ascending())
    self.assertEqual(None, mapping)

  def test_with_slippages(self):
    a17_19 = SObject.Create(17, 18, 19)
    a19_21 = SObject.Create(19, 20, 21)

    controller = Controller()
    mapping = SubspaceFindMapping(controller, 10, left=a17_19, right=a19_21,
                                  category=Ascending())
    self.assertTrue(isinstance(mapping, StructuralMapping))
    self.assertEqual(Ascending(), mapping.category)
    slippages_dict = dict(mapping.slippages)
    self.assertEqual('end', slippages_dict['start'])
