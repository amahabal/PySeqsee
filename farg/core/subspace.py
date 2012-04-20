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

from farg.core.controller import Controller
from farg.core.exceptions import AnswerFoundException, NoAnswerException

class QuickReconnResults:
  """Result of quick reconnaisance before really starting a subspace. Can be one of three
     things:

     * Deepeer exploration is needed.
     * Exploration not needed. An answer has been found.
     * Exploration not needed. No answer is likely to be found.
  """

  kDeeperExplorationNeeded = 1
  kAnswerFound = 2
  kAnswerCannotBeFound = 3

  def __init__(self, state, *, answer=None):
    self.state = state
    self.answer = answer

  @staticmethod
  def DeeperExplorationNeeded():
    return QuickReconnResults(QuickReconnResults.kDeeperExplorationNeeded)

  @staticmethod
  def AnswerFound(answer):
    return QuickReconnResults(QuickReconnResults.kAnswerFound, answer=answer)

  @staticmethod
  def NoAnswerCanBeFound():
    return QuickReconnResults(QuickReconnResults.kAnswerCannotBeFound)


class Subspace:
  controller_class = Controller

  def __init__(self, parent_controller, *, nsteps=5, workspace_arguments=None):
    """Initializes the subspace by just storing the arguments."""
    self.parent_controller = parent_controller
    self.nsteps = nsteps
    self.workspace_arguments = workspace_arguments

  def Run(self):
    """Runs the subspace by first trying to quickly estimate need for deeper exploration.

       If deeper exploration is called for, sets up the controller, workspace, and so forth,
       and runs the controller for upto the specified number of steps.
    """
    quick_reconn_result = self.QuickReconn()
    if quick_reconn_result.state == QuickReconnResults.kAnswerFound:
      return quick_reconn_result.answer
    elif quick_reconn_result.state == QuickReconnResults.kAnswerCannotBeFound:
      return None

    # So we need deeper exploration.
    parent_controller = self.parent_controller
    self.controller = self.controller_class(
        ui=parent_controller.ui,
        controller_depth=(parent_controller.controller_depth + 1),
        workspace_arguments=self.workspace_arguments,
        parent_controller=parent_controller)
    self.InitializeCoderack()
    try:
      self.controller.RunUptoNSteps(self.nsteps)
    except AnswerFoundException as e:
      return e.answer
    except NoAnswerException:
      return None
    return None

  def QuickReconn(self):
    return QuickReconnResults(QuickReconnResults.kDeeperExplorationNeeded)

  def InitializeCoderack(self):
    raise Exception(
        'InitializeCoderack from class Subspace called. This is surely a bug: this method'
        'should have been overridden in a derived class to set up the initial codelet.')
