import unittest
from apps.seqsee.workspace import Workspace
from apps.seqsee.util import LessThan, LessThanEq, GreaterThan, GreaterThanEq, Exactly
from apps.seqsee.sobject import SAnchored, SObject
from farg.exceptions import FargError, ConflictingGroupException

def helper_create_and_insert_group(ws, specification):
  """Utility for quickly creating groups.
  
  Each element in the specification is a tuple consisting of integers or of other similarly
  structured tuples. Each generates a group, where the integers correspond to position in the
  workspace.
  
  A degenerate case is when the specification is an integer, in which case the WS element is
  returned.
  """
  if isinstance(specification, int):
    return ws.elements[specification]
  else:
    anchored_items = list(helper_create_and_insert_group(ws, x) for x in specification)
    new_group = SAnchored.Create(*anchored_items)
    ws.InsertGroup(new_group)
    return new_group

def helper_create_and_insert_groups(ws, *specifications):
  """Utility for quickly creating many groups."""
  for specification in specifications:
    helper_create_and_insert_group(ws, specification)

def helper_create_group_given_spans_of_items(ws, *spans):
  anchored_items = []
  for span in spans:
    if isinstance(span, int):
      anchored_items.append(ws.elements[span])
    else:
      matching_groups = ws.GetGroupsWithSpan(Exactly(span[0]), Exactly(span[1]))
      anchored_items.append(matching_groups.next())
  return SAnchored.Create(*anchored_items)

class TestWorkspace(unittest.TestCase):
  def test_sanity(self):
    ws = Workspace()
    self.assertEqual(0, ws.num_elements)

    ws.InsertElement(SObject.Create(5))
    self.assertEqual(1, ws.num_elements)
    self.assertEqual(5, ws.elements[0].object.magnitude)

    ws.InsertElements(6, 7)
    self.assertEqual(6, ws.elements[1].object.magnitude)
    self.assertEqual((1, 1), ws.elements[1].Span())
    self.assertEqual(3, ws.num_elements)

  def test_insert_group(self):
    ws = Workspace()
    ws.InsertElements(5, 6)
    gp = SAnchored.Create(*ws.elements[:])
    self.assertEqual((0, 1), gp.Span())
    self.assertEqual((5, 6), gp.Structure())

    ws.InsertGroup(gp)
    self.assertEqual(1, len(ws.groups))

  def test_conflicting_groups_simple(self):
    ws = Workspace()
    ws.InsertElements(*range(0, 10))
    helper_create_and_insert_groups(ws, (1, 2, 3), (4, 5, 6))
    self.assertEqual(2, len(ws.groups))

    # An overlapping group not subsumed is fine:
    self.assertFalse(
        tuple(ws.GetConflictingGroups(helper_create_group_given_spans_of_items(ws, 2, 3, 4))))

    # Subsumed that is not an element is problematic.
    self.assertTrue(
        tuple(ws.GetConflictingGroups(helper_create_group_given_spans_of_items(ws, 2, 3))))

    # But if subsumed *is* an element, that is okay.
    self.assertFalse(
        tuple(ws.GetConflictingGroups(helper_create_group_given_spans_of_items(ws, 2))))

  def test_conflicting_groups_more_complex(self):
    ws = Workspace()
    ws.InsertElements(*range(0, 10))
    helper_create_and_insert_groups(ws, ((1, 2, 3), (4, 5, 6), (7, 8)))
    self.assertEqual(4, len(ws.groups))

    # An overlapping group not subsumed is fine:
    self.assertFalse(
        tuple(ws.GetConflictingGroups(
                  helper_create_group_given_spans_of_items(ws, 0, (1, 3), 4))))
    self.assertFalse(
        tuple(ws.GetConflictingGroups(helper_create_group_given_spans_of_items(ws, 0, (1, 3)))))

    # Subsumed that is not an element is problematic.
    self.assertTrue(
        tuple(ws.GetConflictingGroups(helper_create_group_given_spans_of_items(
            ws, (1, 3), (4, 6)))))

    # But if subsumed *is* an element, that is okay.
    # Here, the group being tested is an *existing* group.
    self.assertFalse(
        tuple(ws.GetConflictingGroups(helper_create_group_given_spans_of_items(ws, (1, 3)))))

    # Note, however, that if a new group is crafted out of existing parts, such that is aligns
    # exactly with an existing group, it is still in conflict.
    g1 = helper_create_group_given_spans_of_items(ws, 1, 2, 3)
    self.assertTrue(ws.GetConflictingGroups(g1))

    self.assertRaises(ConflictingGroupException, ws.InsertGroup, g1)

  def test_supergroups(self):
    ws = Workspace()
    ws.InsertElements(*range(0, 10))
    helper_create_and_insert_groups(ws, ((1, 2, 3), (4, 5, 6), (7, 8)))
    self.assertEqual(1, len(tuple(ws.GetSuperGroups(ws.elements[1]))))
    g1 = helper_create_group_given_spans_of_items(ws, (1, 3))
    self.assertEqual(1, len(tuple(ws.GetSuperGroups(g1))))
    helper_create_and_insert_groups(ws, (3, 4, 5))
    g2 = helper_create_group_given_spans_of_items(ws, (3, 5))
    self.assertEqual(0, len(tuple(ws.GetSuperGroups(g2))))
    self.assertEqual(2, len(tuple(ws.GetSuperGroups(ws.elements[3]))))

