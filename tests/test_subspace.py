import unittest

from apps.seqsee.sobject import SObject
from apps.seqsee.categories import Ascending
from apps.seqsee.mapping import StructuralMapping
from farg.controller import Controller
from farg.exceptions import FargException, AnswerFoundException
from farg.run_state import RunState

class Subspace(object):
  """A base class for subspaces."""

  @classmethod
  def QuickReconnaisance(cls, arguments):
    return { 'answer_found': False }

  def __init__(self):
    self.run_state = RunState()
    self.controller = Controller(self.run_state)

class SubspaceFindMapping(Subspace):
  class Workspace():
    def __init__(self, left, right, category):
      self.left = left
      self.right = right
      self.category = category

  def Initialize(self, arguments):
    self.workspace = self.run_state.workspace = self.Workspace(**arguments)

  @classmethod
  def QuickReconnaisance(cls, arguments):
    mapping = arguments['category'].GetMapping(arguments['left'], arguments['right'])
    if mapping:
      return { 'answer_found': True, 'answer': mapping }
    return None

def Subtask(subspace_class, max_number_of_steps, arguments):
  """The driver for subtask calculations: creates a subspace based on class and arguments, and
  runs it to a maximum of max_number_of_steps, returning None or an appropriate result."""
  quick_result = subspace_class.QuickReconnaisance(arguments)
  if not quick_result:
    return None
  if quick_result['answer_found']:
    return quick_result['answer']
  subspace = subspace_class()
  subspace.Initialize(arguments)
  try:
    subspace.controller.RunUptoNSteps(max_number_of_steps)
  except AnswerFoundException as e:
    return e.answer
  return None

class TestSubspace(unittest.TestCase):
  def test_sanity(self):
    # This test refers to things in the Seqsee app. Maybe the test should move there.
    a3 = SObject.Create(1, 2, 3)
    a4 = SObject.Create(1, 2, 3, 4)
    a5 = SObject.Create(1, 2, 3, 4, 5)

    a17_19 = SObject.Create(17, 18, 19)
    a19_21 = SObject.Create(19, 20, 21)

    mapping = Subtask(SubspaceFindMapping, 3, { 'left': a3, 'right': a4, 'category': Ascending})
    self.assertTrue(isinstance(mapping, StructuralMapping))
    self.assertEqual(Ascending, mapping.category)
    self.assertEqual(None, mapping.slippages)

    mapping = Subtask(SubspaceFindMapping, 3, { 'left': a5,
                                                'right': a19_21,
                                                'category': Ascending})
    self.assertEqual(None, mapping)

#    mapping = Subtask(SubspaceFindMapping, 3, { 'left': a17_19,
#                                                'right': a19_21,
#                                                'category': Ascending})
#    self.assertTrue(isinstance(mapping, StructuralMapping))
#    self.assertEqual(Ascending, mapping.category)
#    self.assertEqual('end', mapping.slippages['start'])
