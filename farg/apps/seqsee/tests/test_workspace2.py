"""Test workspace more thoroughly."""

import unittest
from farg.apps.seqsee.anchored import SAnchored
from farg.apps.seqsee.sobject import SObject, SElement, LTMStorableSObject
from farg.apps.seqsee.workspace import Workspace
from farg.core.ltm.storable import LTMStorableMixin
from farg.core.categorization.categorizable import CategorizableMixin
from farg.apps.seqsee.categories import Prime
from farg.apps.seqsee.relation import Relation

class TestWorkspace(unittest.TestCase):
  
  def setUp(self):
    self.ws = ws = Workspace()
    ws.InsertElements((5, 6, 7, 8))
    ws.InsertGroup(SAnchored.Create((ws.elements[0], ws.elements[1])))

  def test_elements(self):
    self.assertEqual(4, self.ws.num_elements)
    e1 = self.ws.elements[0]
    self.assertIsInstance(e1.object, SElement)
    self.assertIsInstance(e1.object, SObject)
    self.assertIsInstance(e1, SAnchored)
    self.assertEqual((0, 0), e1.Span())
    self.assertTrue(e1.is_sequence_element)
    self.assertEqual(5, e1.object.magnitude)

  def test_groups(self):
    self.assertEqual(1, len(self.ws.groups))
    gp = list(self.ws.groups)[0]
    self.assertIsInstance(gp.object, SObject)
    self.assertIsInstance(gp, SAnchored)
    self.assertEqual((0, 1), gp.Span())
    self.assertFalse(gp.is_sequence_element)
    self.assertEqual((5, 6), gp.object.Structure())

  def test_group_overlap(self):
    # We can create a second group at same location
    ws = self.ws
    gp = list(ws.groups)[0]
    gp_cp = SAnchored.Create((ws.elements[0], ws.elements[1]))
    self.assertNotIn(gp_cp, ws.groups, "gp_cp not yet part of workspace")
    self.assertNotEqual(gp, gp_cp, "The two groups differ")
    
    gp2 = SAnchored.Create(ws.elements[:])
    self.assertIn(gp, ws.GetConflictingGroups(gp2))
    
    gp3 = SAnchored.Create((ws.elements[1], ws.elements[2]))
    # Overlap does not constitute conflict.
    self.assertNotIn(gp, ws.GetConflictingGroups(gp3))
    
    # Also, groups do not conflict with others at exactly the same location if their structures are
    # identical.
    self.assertNotIn(gp, ws.GetConflictingGroups(gp_cp))
    
    # However, [[X, Y], Z] SHOULD conflict [X, [Y, Z]]
    gp_XY_Z = ws.InsertGroup(SAnchored.Create((gp, ws.elements[2])))
    gp_X_YZ = SAnchored.Create((ws.elements[0], gp3))
    self.assertIn(gp_XY_Z, ws.GetConflictingGroups(gp_X_YZ))
    
    

  def test_ltm_storability(self):
    gp = list(self.ws.groups)[0]
    self.assertIsInstance(gp, LTMStorableMixin)
    storable = gp.GetLTMStorableContent()
    self.assertIsInstance(storable, LTMStorableSObject)
    self.assertEqual((5, 6), storable.structure)
    self.assertEqual(gp.GetLTMStorableContent(), storable, "Repeated call gives same value.")
    
    # A different group with the same structure will also give the same storable.
    self.assertEqual(SAnchored.Create((self.ws.elements[0],
                                       self.ws.elements[1])).GetLTMStorableContent(), storable)

  def test_object_categorizability(self):
    ws = self.ws
    el0 = ws.elements[0]
    self.assertIsInstance(el0.object, CategorizableMixin)
    binding = el0.object.DescribeAs(Prime())
    self.assertEqual({'index': 2}, binding.bindings)

  def test_relations(self):
    # I will insert a relation between two groups, test its existence, and then delete one group.
    # The relation should disappear.
    gp = list(self.ws.groups)[0]
    gp2 = self.ws.InsertGroup(SAnchored.Create(self.ws.elements[2:4]))
    rel = Relation(gp, gp2, mapping_set=set())
    rel.InsertSelf()
    self.assertIn(rel, gp.relations, "Ends contain relation")
    self.assertIn(rel, gp2.relations, "Ends contain relation")
    
    # Now let's delete gp2: gp should have no relations left.
    self.assertEqual(2, len(self.ws.groups))
    self.ws.DeleteGroup(gp2)
    self.assertEqual(1, len(self.ws.groups))
    self.assertNotIn(rel, gp.relations, "End no longer contains relation")
