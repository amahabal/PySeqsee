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
"""Viewport defines a section of a canvas for displaying some information.

The coordinates (left, top) and (bottom, right) define a rectangular section of the canvas.

This is an abstract class where a few methods need to be plugged in.
"""

from abc import ABCMeta, abstractmethod    # Metaclass confuses pylint: disable=W0611


class ViewPort(metaclass=ABCMeta):
  """Viewport defines a section of a canvas for displaying some information."""

  def __init__(self, canvas, left, bottom, width, height):
    """Defines section of a canvas for displaying the list.

    Args:
      canvas: Canvas where the view is drawn.
      left:
      bottom:
      width:
      height: Define the section of the canvas where view will be drawn.
    """
    self.left = left
    self.bottom = bottom
    self.height = height
    self.width = width
    self.canvas = canvas

  def CanvasCoordinates(self, x, y):
    """Converts coordinates in this view to canvas coordinates."""
    return (self.left + x, self.bottom + y)

  @abstractmethod
  def ReDraw(self, controller):
    """Redraw this view.

    Args:
      controller: The controller for the main application.
    """
    pass
