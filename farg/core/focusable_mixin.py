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

from farg.core.exceptions import FargError
class FocusableMixin(object):
  """A mixin for things that want to be part of the stream. It is a pure interface --- all
     methods die horribly when called since they expect to have been over-ridden.
  """


  def GetFringe(self, controller):
    """Returns the fringe of the item, which should be a dictionary keyed by fringe elements
       and with floats as values (indicating intensity of the element within the fringe).
    """
    raise FargError("Focusable mixin's GetFringe() was not over-ridden.")


  def GetAffordances(self, controller):
    """Returns a list of codelets that make sense for this type of object."""
    raise FargError("Focusable mixin's GetAffordances() was not over-ridden.")


  def GetSimilarityAffordances(self, focusable, other_fringe, my_fringe, controller):
    """When the fringe of a stored focus overlaps the fringe of a newly focused entity,
       this function is called. Here, self is the older focus, and my_fringe is its fringe.
       focusable is the new focusable, and other_fringe is its fringe.
       
       This should return a list of codelets that follow-up on this potential similarity.
    """
    raise FargError("Focusable mixin's GetSimilarityAffordances() was not over-ridden.")

  def OnFocus(self, controller):
    """Any book-keeping or other sundry actions on focused-upon object may be done here."""
    pass
