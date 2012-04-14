# Copyright (C) 2011, 2012  Abhijit Mahabal

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

from farg.controller import Controller
from farg.meta import SubspaceMeta

class Subspace(metaclass=SubspaceMeta):
  controller_class = Controller

  @staticmethod
  def QuickReconn(**args):
    raise Exception("Attempt to call Subspace(). Surely you meant to call a subclass?")

  def InitializeCoderack(self):
    raise Exception("Base InitializeCoderack called. This should have been overridden "
                    "(to set up the initial codelet, for example)")

  def RoutineCodeletsToAdd(self):
    return None

  def __init__(self, parent_controller, nsteps, workspace_arguments):
    self.controller = self.controller_class(
        ui=parent_controller.ui,
        controller_depth=(parent_controller.controller_depth + 1),
        workspace_arguments=workspace_arguments,
        parent_controller=parent_controller)
    self.max_number_of_steps = nsteps
    self.InitializeCoderack()

  def Run(self):
    self.controller.RunUptoNSteps(self.max_number_of_steps)
