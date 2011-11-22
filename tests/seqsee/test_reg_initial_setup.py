import unittest

from apps.seqsee.sobject import SAnchored, SElement, SGroup
from apps.seqsee.runstate import SeqseeRunState
from apps.seqsee.workspace import Workspace
from components.coderack import Coderack
from components.stream import Stream

class TestRegtestInitialSetup(unittest.TestCase):
  def test_sanity(self):
    runstate = SeqseeRunState()
    self.assertTrue(isinstance(runstate.ws, Workspace))
    self.assertTrue(isinstance(runstate.coderack, Coderack))
    self.assertTrue(isinstance(runstate.stream, Stream))

    self.assertEqual(0, runstate.coderack._codelet_count)

  def test_ws(self):
    runstate = SeqseeRunState()
    ws = runstate.ws
    cr = runstate.coderack
    ws.InsertElements(1, 1, 2, 1, 2, 3)
    self.assertEqual(6, ws.num_elements)

    first_el = ws.elements[0]
    self.assertTrue(isinstance(first_el, SAnchored))
    self.assertTrue(isinstance(first_el.object, SElement))
    self.assertEqual(1, first_el.object.magnitude)
    self.assertEqual(0, first_el.start_pos)
    self.assertEqual(0, first_el.end_pos)
    self.assertTrue(first_el.is_sequence_element)
    self.assertFalse(first_el.items)

    gp = SAnchored.Create(ws.elements[1], ws.elements[2])
    self.assertTrue(isinstance(gp, SAnchored))
    self.assertTrue(isinstance(gp.object, SGroup))
    self.assertEqual((1, 2), gp.object.Structure())
    self.assertEqual(1, gp.start_pos)
    self.assertEqual(2, gp.end_pos)
    self.assertFalse(gp.is_sequence_element)
    self.assertEqual(tuple(ws.elements[1:3]), gp.items)
