from farg.subspace import Subspace
from farg.exceptions import AnswerFoundException
from farg.util import WeightedChoice

def ThingsToChooseFrom(ws):
  """Yields two-tuples of things to choose from, the second being weight."""
  # QUALITY TODO(Feb 14, 2012): This should be a subspace. What do we choose from, what
  # to pay attention to?
  # QUALITY TODO(Feb 14, 2012): Explore role of relations.
  # TODO(#34 --- Dec 28, 2011): Need notion of strength. Will bias these weights.
  for element in ws.elements:
    yield (element, 0.5)
  for gp in ws.groups:
    yield (gp, 1.0)

class SubspaceSelectObjectToFocusOn(Subspace):
  class WS(object):
    def __init__(self, parent_ws):
      self.parent_ws = parent_ws


  @staticmethod
  def QuickReconn(**arguments):
    raise AnswerFoundException(WeightedChoice(ThingsToChooseFrom(arguments['parent_ws'])))
