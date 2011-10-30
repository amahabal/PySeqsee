import unittest
from apps.seqsee.workspace import Workspace
from apps.seqsee.sobject import SAnchored, SObject

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
      anchored_items.append(ws.GetGroupWithSpan(*span))
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
        ws.GetConflictingGroups(helper_create_group_given_spans_of_items(ws, 2, 3, 4)))

    self.assertTrue(
        ws.GetConflictingGroups(helper_create_group_given_spans_of_items(ws, 2, 3)))




