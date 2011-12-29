from farg.controller import Controller
from farg.exceptions import FargException, AnswerFoundException, NoAnswerException

class QuickReconnaisanceResult(object):
  """QuickReconnaisance looks at the input to the subspace and makes a quick, rough
     judgement about whether an answer might even be possible or sometimes quickly finds
     the answer. The determination can thus take three forms:
     
       * No answer likely.
       * Answer found, and here it is.
       * More exploration needed.
  """

  def __init__(self, answer_likely=True, answer=None):
    self.answer_likely = answer_likely
    self.answer = answer

  def NoAnswerLikely(self):
    """Returns true if the result is that no answer is likely."""
    return not(self.answer_likely)

  def AnswerFound(self):
    return self.answer is not None


def AnswerFound(answer):
  return QuickReconnaisanceResult(answer=answer)

NeedDeeperExploration = QuickReconnaisanceResult()
NoAnswerLikely = QuickReconnaisanceResult(answer_likely=False)

class Subspace(object):
  """A base class for subspaces."""

  @classmethod
  def QuickReconnaisance(cls, arguments):
    return NeedDeeperExploration()

  @classmethod
  def RoutineCodeletsToAdd(cls):
    return None

  def __init__(self):
    self.controller = Controller(routine_codelets_to_add=self.RoutineCodeletsToAdd())

def Subtask(subspace_class, max_number_of_steps, arguments):
  """The driver for subtask calculations: creates a subspace based on class and arguments,
     and runs it to a maximum of max_number_of_steps, returning None or an appropriate
     result.
  """
  # TODO(#17 --- Dec 28, 2011): Better documentation with examples.
  quick_result = subspace_class.QuickReconnaisance(arguments)
  if quick_result.NoAnswerLikely():
    return None
  if quick_result.AnswerFound():
    return quick_result.answer
  if not max_number_of_steps:
    return None
  subspace = subspace_class()
  subspace.Initialize(arguments)
  try:
    subspace.controller.RunUptoNSteps(max_number_of_steps)
  except AnswerFoundException as e:
    return e.answer
  except NoAnswerException:
    return None
  return None
