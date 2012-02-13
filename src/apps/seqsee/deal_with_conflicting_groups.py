from farg.subspace import Subspace
from farg.codelet import CodeletFamily
from farg.util import Toss
from farg.exceptions import NoAnswerException

class CF_FightIncumbents(CodeletFamily):
  @classmethod
  def Run(cls, controller):
    # QUALITY TODO(Feb 12, 2012): Strengths of groups are important. Need to work those in.
    ws = controller.workspace
    parent_ws = controller.parent_controller.workspace
    for incumbent in ws.incumbents:
      if Toss(0.3):  # QUALITY TODO(Feb 12, 2012): Surely, I can do better :)
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
