import unittest
from apps.seqsee.workspace import Workspace
from apps.seqsee.sobject import SAnchored, SObject


class TestWorkspace(unittest.TestCase):
  def test_sanity(self):
    ws = Workspace()
    self.assertEqual(0, ws.num_elements)

    ws.InsertElement(SObject.Create(5))
    self.assertEqual(1, ws.num_elements)
    self.assertEqual(5, ws.elements[0].object.magnitude)

    ws.InsertElement(SObject.Create(6))
    self.assertEqual(6, ws.elements[1].object.magnitude)
