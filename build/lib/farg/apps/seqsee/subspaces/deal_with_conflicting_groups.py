# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

from farg.core.codelet import CodeletFamily
from farg.core.controller import Controller
from farg.core.exceptions import NoAnswerException
from farg.core.subspace import Subspace
from farg.core.util import Toss

class CF_FightIncumbents(CodeletFamily):
  @staticmethod
  def ProbabilityOfOverturningIncumbent(incumbent_strength, challenger_strength):
    if not incumbent_strength:
      return 0.6
    return 0.6 * (challenger_strength / (incumbent_strength + challenger_strength))

  @classmethod
  def Run(cls, controller):
    # QUALITY TODO(Feb 12, 2012): Strengths of groups are important. Need to work those in.
    workspace = controller.workspace
    parent_ws = controller.parent_controller.workspace
    challenger_strength = workspace.new_group.strength
    for incumbent in workspace.incumbents:
      probability_of_deletion = CF_FightIncumbents.ProbabilityOfOverturningIncumbent(
          incumbent.strength,
          challenger_strength)
      if Toss(probability_of_deletion):
        parent_ws.DeleteGroup(incumbent)
      else:
        raise NoAnswerException(codelet_count=controller.steps_taken)
    # Okay, I suppose we can plonk this in.
    parent_ws._PlonkIntoPlace(workspace.new_group)

class SubspaceDealWithConflictingGroups(Subspace):
  class controller_class(Controller):
    class workspace_class:
      def __init__(self, new_group, incumbents):
        self.new_group = new_group
        self.incumbents = incumbents

  def InitializeCoderack(self):
    self.controller.AddCodelet(family=CF_FightIncumbents, urgency=100)
