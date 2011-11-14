import unittest

from apps.seqsee.run_state import SeqseeRunState
from apps.seqsee.workspace import Workspace
from components.coderack import Coderack
from components.stream import Stream

class TestRegtestInitialSetup(unittest.TestCase):
  def test_sanity(self):
    run_state = SeqseeRunState()
    self.assertTrue(isinstance(run_state.ws, Workspace))
    self.assertTrue(isinstance(run_state.coderack, Coderack))
    self.assertTrue(isinstance(run_state.stream, Stream))

    self.assertEqual(0, run_state.coderack._codelet_count)

  def test_ws(self):
    run_state = SeqseeRunState()
    ws = run_state.ws
    cr = run_state.coderack
    ws.InsertElements(1, 1, 2, 1, 2, 3)
    self.assertEqual(6, ws.num_elements)
