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
from farg.core.subspace import Subspace, QuickReconnResults
import farg.flags as farg_flags
class SubspaceAreWeDone(Subspace):
  """Checks if we should stop because we have found or explained the answer.

     Currently a hack, stops when 10 new terms have been correctly predicted.
  """
  from farg.core.controller import Controller
  controller_class = Controller

  def quick_reconn(self):
    parent_ws = self.parent_controller.workspace
    current_known_elements = parent_ws.num_elements
    initial_known_elements = len(farg_flags.FargFlags.sequence)
    if current_known_elements >= initial_known_elements + 10:
      return QuickReconnResults.answer_found(True)
    else:
      return QuickReconnResults.answer_found(False)
