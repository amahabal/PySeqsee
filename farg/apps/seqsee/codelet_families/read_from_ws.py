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

from farg.apps.seqsee.subspaces.choose_item_to_focus_on import SubspaceSelectObjectToFocusOn
from farg.core.codelet import CodeletFamily
class CF_ReadFromWS(CodeletFamily):
  """Read an item from the WS and focus on it.
  """
  @classmethod
  def Run(cls, controller, *, me):
    choice = SubspaceSelectObjectToFocusOn(controller).Run()
    if choice:
      controller.stream.FocusOn(choice, parents=[me])
