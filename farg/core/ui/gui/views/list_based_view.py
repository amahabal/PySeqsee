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

"""Defines a class that can act as a base class for displaying lists of things.

Examples of such things include codelets in a coderack and recent foci in the stream.
"""
from abc import ABCMeta, abstractmethod    # Metaclass confuses pylint: disable=W0611
from farg.core.ui.gui.views.viewport import ViewPort
from math import ceil
from tkinter import NE, NW


class ListBasedView(ViewPort, metaclass=ABCMeta):
  """A base class for views that show a bunch of objects and which require pagination."""

  #: Number of items to show per page.
  items_per_page = 5    # Not a constant as thought by pylint: disable=C6409

  def __init__(self, canvas, left, bottom, width, height):
    """Defines section of a canvas for displaying the list.

    Args:
      canvas: Canvas where the view is drawn.
      left:
      bottom:
      width:
      height: Define the section of the canvas where view will be drawn.
    """
    ViewPort.__init__(self, canvas, left, bottom, width, height)
    self.height_per_row = 0.8 * (height - 20) / self.items_per_page
    self.current_page_number = 1

  def _ClearAndRedraw(self):
    """Redraw entire canvas (not just this view.

    Called when some action has been taken where a full refresh may make sense.
    """
    self.canvas.ReDraw()

  def _IncrementPageNumber(self):
    """Increases the page number."""
    self.current_page_number += 1
    self._ClearAndRedraw()

  def _DecrementPageNumber(self):
    """Decreases the page number."""
    assert(self.current_page_number > 1)
    self.current_page_number -= 1
    self._ClearAndRedraw()

  def _DrawPreviousPageArrow(self):
    """Draw a triangle facing left hooked to decrementing the page number."""
    x1, y1 = self.CanvasCoordinates(0, 10)
    x2, y2 = self.CanvasCoordinates(15, 0)
    x3, y3 = self.CanvasCoordinates(15, 20)
    item_id = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3)
    self.canvas.tag_bind(item_id, '<1>', lambda e: self._DecrementPageNumber())

  def _DrawNextPageArrow(self):
    """Draw a triangle facing left hooked to incrementing the page number."""
    width = self.width
    x1, y1 = self.CanvasCoordinates(width, 10)
    x2, y2 = self.CanvasCoordinates(width - 15, 0)
    x3, y3 = self.CanvasCoordinates(width - 15, 20)
    item_id = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3)
    self.canvas.tag_bind(item_id, '<1>', lambda e: self._IncrementPageNumber())

  def ReDrawView(self, controller):
    """Redraw this view.

    Args:
      controller: The controller for the main application.
    """
    self.canvas.create_rectangle(self.left, self.bottom,
                                 self.left + self.width, self.bottom + self.height,
                                 fill='#EEEEFF', outline='#CCCCFF')
    items, top_message, extra_dict = self.GetAllItemsToDisplay(controller)
    items_count = len(items)
    max_page_number = ceil(1.0 * items_count / self.items_per_page)
    if self.current_page_number > max_page_number:
      self.current_page_number = 1
    index_of_first_item = (self.current_page_number - 1) * self.items_per_page
    index_beyond_last_item = index_of_first_item + self.items_per_page
    if index_beyond_last_item > items_count:
      index_beyond_last_item = items_count
    items_to_show = items[index_of_first_item:index_beyond_last_item]
    x, y = self.CanvasCoordinates(20, 0)
    self.canvas.create_text(x, y, text=top_message, anchor=NW, fill='#3333FF')

    if max_page_number > 0:
      x, y = self.CanvasCoordinates(self.width - 25, 0)
      self.canvas.create_text(x, y,
                              text='p. %d/%d' % (self.current_page_number, max_page_number),
                              anchor=NE, fill='#33FF33')

    row_top_y = 20
    for item in items_to_show:
      self.DrawItem(20, row_top_y, item, extra_dict, controller)
      row_top_y += self.height_per_row

    if self.current_page_number > 1:
      self._DrawPreviousPageArrow()

    if self.current_page_number < max_page_number:
      self._DrawNextPageArrow()

  @abstractmethod
  def GetAllItemsToDisplay(self, controller):
    """Obtain a 3-tuple (items, top-message, extra_dict) to display.

    Should be over-ridden by the derived class.

    Args:
      controller: The controller for the main application.

    Returns:
      A 3-tuple. The first value is a list of items to display (on all pages). The second
      is a message to be displayed at the top. The third is a dictionary for passing in
      arbitrary information, which is passed on to DrawItem.
    """
    pass

  @abstractmethod
  def DrawItem(self, x, y, item, extra_dict, controller):
    """Draws item given co-ordinates in *this* widgets coordinate system.

    Args:
      x: x-coordinate for the top-left, within this view, where the item is to be drawn.
      y: y-coordinate for the top-left, within this view, where the item is to be drawn.
      item: item to be drawn.
      extra_dict: Any extra key-value pairs to be passed in to influence the display.
      controller: The controller for the main application.
    """
    pass
