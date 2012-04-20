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

class ViewPort(object):
  def __init__(self, canvas, left, bottom, width, height):
    self.left = left
    self.bottom = bottom
    self.height = height
    self.width = width
    self.canvas = canvas

  def ReDraw(self, controller):
    # Should delete things with particular identifiers. I will let canvas delete, for now.
    self.ReDrawView(controller)

  def CanvasCoordinates(self, x, y):
    return (self.left + x, self.bottom + y)
