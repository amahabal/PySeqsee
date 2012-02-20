from farg.subspace import Subspace
from farg.codelet import CodeletFamily
from farg.util import Toss
from farg.exceptions import NoAnswerException

class CF_FightIncumbents(CodeletFamily):
  @staticmethod
  def ProbabilityOfOverturningIncumbent(incumbent_strength, challenger_strength):
    if not incumbent_strength:
      return 0.6
    return 0.6 * (challenger_strength / (incumbent_strength + challenger_strength))

  @classmethod
  def Run(cls, controller):
    # QUALITY TODO(Feb 12, 2012): Strengths of groups are important. Need to work those in.
    ws = controller.workspace
    parent_ws = controller.parent_controller.ws
    challenger_strength = ws.new_group.strength
    for incumbent in ws.incumbents:
      probability_of_deletion = CF_FightIncumbents.ProbabilityOfOverturningIncumbent(
          incumbent.strength,
          challenger_strength)
      if Toss(probability_of_deletion):
        parent_ws.DeleteGroup(incumbent)
      else:
        raise NoAnswerException()
    # Okay, I suppose we can plonk this in.
    parent_ws._PlonkIntoPlace(ws.new_group)

class SubspaceDealWithConflictingGroups(Subspace):
  class WS(object):
    def __init__(self, new_group, incumbents):
      self.new_group = new_group
      self.incumbents = incumbents

  @staticmethod
  def QuickReconn(**arguments):
    pass

  def InitializeCoderack(self, controller):
    controller.AddCodelet(CF_FightIncumbents, 100)
    controller.DisplayMessage("Initialized a SubspaceDealWithConflictingGroups")
