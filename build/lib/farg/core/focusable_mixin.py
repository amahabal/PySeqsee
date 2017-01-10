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
"""Mixin class to be added to anything that can be the focus in the stream."""

from abc import ABCMeta, abstractmethod  # Metaclass confuses pylint: disable=W0611


class FocusableMixin(metaclass=ABCMeta):
  """A mixin for things that want to be part of the stream.

   It is a pure interface --- all methods die horribly when called unless over-ridden.
  """

  def __init__(self):
    pass

  @abstractmethod
  def GetFringe(self, controller):
    """Returns the fringe of the item.

    Args:
      controller: controller for this subspace (or whole app if this is the top space).

    Returns:
      A dictionary keyed by fringe elements and with floats as values (indicating intensity
      of the element within the fringe).
    """
    pass

  @abstractmethod
  def GetAffordances(self, controller):
    """Returns a list of codelets that make sense for this type of object.

    Args:
      controller: controller for this subspace (or whole app if this is the top space).

    Returns:
      A list of codelets for actions that may be taken on this focusable.
    """
    pass

  @abstractmethod
  def GetSimilarityAffordances(self, focusable, other_fringe, my_fringe, controller):
    """Potential actions to take in response to a fringe overlap.

    When the fringe of a stored focus overlaps the fringe of a newly focused entity,
    this function is called. Here, self is the older focus, and my_fringe is its fringe.
    focusable is the new focusable, and other_fringe is its fringe.

    Args:
      focusable: The most recent focus.
      other_fringe: Fringe of 'focusable'.
      my_fringe: Fringe of 'self', which is the older focusable.
      controller: controller for this subspace (or whole app if this is the top space).

    Returns:
      A list of codelets that follow-up on this potential similarity.
    """
    pass

  def OnFocus(self, controller):
    """Any book-keeping or other sundry actions on focused-upon object may be done here.

    Args:
      controller: controller for this subspace (or whole app if this is the top space).
    """
    pass
