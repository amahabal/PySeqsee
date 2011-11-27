from farg.controller import Controller
from farg.exceptions import FargException, AnswerFoundException, NoAnswerException

def AnswerFound(answer):
  return { 'answer_found': True, 'answer': answer}

def NeedDeeperExploration():
  return { 'answer_found': False }

def NoAnswerLikely():
  return None

class Subspace(object):
  """A base class for subspaces."""

  @classmethod
  def QuickReconnaisance(cls, arguments):
    return NeedDeeperExploration()

  def __init__(self):
    self.controller = Controller()

def Subtask(subspace_class, max_number_of_steps, arguments):
  """The driver for subtask calculations: creates a subspace based on class and arguments, and
  runs it to a maximum of max_number_of_steps, returning None or an appropriate result."""
  quick_result = subspace_class.QuickReconnaisance(arguments)
  if not quick_result:
    return None
  if quick_result['answer_found']:
    return quick_result['answer']
  if not max_number_of_steps:
    return None
  subspace = subspace_class()
  subspace.Initialize(arguments)
  try:
    subspace.controller.RunUptoNSteps(max_number_of_steps)
  except AnswerFoundException as e:
    return e.answer
  return None
