from farg.apps.seqsee import run_seqsee
from farg.apps.seqsee.anchored import SAnchored
from farg.apps.seqsee.controller import SeqseeController
from farg.apps.seqsee.sobject import SElement, SGroup
from farg.apps.seqsee.workspace import Workspace
from farg.core.coderack import Coderack
from farg.core.stream import Stream
from farg.core.ui.batch_ui import BatchUI
from farg.third_party import gflags
import threading
import unittest

FLAGS = gflags.FLAGS

FLAGS.sequence = []
FLAGS.unrevealed_terms = []

class TestRegtestInitialSetup(unittest.TestCase):
  def test_sanity(self):
    ui = BatchUI(controller_class=SeqseeController)
    controller = SeqseeController(ui=ui, controller_depth=0)
    self.assertTrue(isinstance(controller.workspace, Workspace))
    self.assertTrue(isinstance(controller.coderack, Coderack))
    self.assertTrue(isinstance(controller.stream, Stream))

    self.assertTrue(controller.coderack._codelet_count > 0)

  def test_ws(self):
    ui = BatchUI(controller_class=SeqseeController)
    controller = SeqseeController(ui=ui, controller_depth=0)
    workspace = controller.workspace
    workspace.InsertElements((1, 1, 2, 1, 2, 3))
    self.assertEqual(6, workspace.num_elements)

    first_el = workspace.elements[0]
    self.assertTrue(isinstance(first_el, SAnchored))
    self.assertTrue(isinstance(first_el.object, SElement))
    self.assertEqual(1, first_el.object.magnitude)
    self.assertEqual(0, first_el.start_pos)
    self.assertEqual(0, first_el.end_pos)
    self.assertTrue(first_el.is_sequence_element)
    self.assertFalse(first_el.items)

    gp = SAnchored.Create(workspace.elements[1], workspace.elements[2])
    self.assertTrue(isinstance(gp, SAnchored))
    self.assertTrue(isinstance(gp.object, SGroup))
    self.assertEqual((1, 2), gp.object.Structure())
    self.assertEqual(1, gp.start_pos)
    self.assertEqual(2, gp.end_pos)
    self.assertFalse(gp.is_sequence_element)
    self.assertEqual(tuple(workspace.elements[1:3]), gp.items)
