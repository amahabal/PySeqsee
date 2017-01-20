from farg.apps.seqsee.categories import Ascending
from farg.apps.seqsee.mapping import StructuralMapping, FindMapping
from farg.apps.seqsee.sobject import SObject
from farg.core.controller import Controller
from farg.core.ui.batch_ui import BatchUI
import unittest
from farg.core.ltm.graph import LTMGraph


class TestSubspace(unittest.TestCase):
  def test_sanity(self):
    # This test refers to things in the Seqsee app. Maybe the test should move there.
    a3 = SObject.Create([11, 12, 13])
    a4 = SObject.Create([11, 12, 13, 14])
    a5 = SObject.Create([11, 12, 13, 14, 15])

    a19_21 = SObject.Create([19, 20, 21])

    _ui = BatchUI(controller_class=Controller)
    controller = _ui.controller
    controller.ltm = LTMGraph(empty_ok_for_test=True)
    mapping = FindMapping(a3, a4, category=Ascending(), controller=controller,
                          seqsee_ltm=controller.ltm)
    self.assertTrue(isinstance(mapping, StructuralMapping))
    self.assertEqual(Ascending(), mapping.category)
    self.assertFalse(mapping.slippages)

    mapping = FindMapping(a5, a19_21, category=Ascending(), controller=controller,
                          seqsee_ltm=controller.ltm)
    self.assertEqual(None, mapping)

  def test_with_slippages(self):
    a17_19 = SObject.Create([17, 18, 19])
    a19_21 = SObject.Create([19, 20, 21])

    _ui = BatchUI(controller_class=Controller)
    controller = _ui.controller
    controller.ltm = LTMGraph(empty_ok_for_test=True)
    mapping = FindMapping(a17_19, a19_21, category=Ascending(), controller=controller,
                          seqsee_ltm=controller.ltm)
    self.assertTrue(isinstance(mapping, StructuralMapping))
    self.assertEqual(Ascending(), mapping.category)
    slippages_dict = dict(mapping.slippages)
    self.assertEqual('end', slippages_dict['start'])
