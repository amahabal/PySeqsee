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

from farg.subspace import QuickReconnResults, Subspace
from farg.util import WeightedChoice

def ThingsToChooseFrom(ws):
  """Yields two-tuples of things to choose from, the second being weight."""
  # QUALITY TODO(Feb 14, 2012): This should be a subspace. What do we choose from, what
  # to pay attention to?
  # QUALITY TODO(Feb 14, 2012): Explore role of relations.
  # TODO(#34 --- Dec 28, 2011): Need notion of strength. Will bias these weights.
  for element in ws.elements:
    yield (element, 20)
  for gp in ws.groups:
    yield (gp, gp.strength)

class SubspaceSelectObjectToFocusOn(Subspace):
  def QuickReconn(self):
    parent_ws = self.parent_controller.workspace
    choice = WeightedChoice(ThingsToChooseFrom(parent_ws))
    if choice:
      return QuickReconnResults.AnswerFound(choice)
    else:
      return QuickReconnResults.NoAnswerCanBeFound()
