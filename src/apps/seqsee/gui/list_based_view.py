from apps.seqsee.gui.viewport import ViewPort
from math import ceil
from Tkinter import NW

class ListBasedView(ViewPort):
  """A base class for views that show a bunch of objects and may require pagination."""

  #: Number of items to show per page.
  items_per_page = 5

  def __init__(self, canvas, left, bottom, width, height):
    ViewPort.__init__(self, canvas, left, bottom, width, height)
    self.height_per_row = 0.8 * (height - 20) / self.items_per_page
    self.current_page_number = 1

  def ClearAndRedraw(self):
    self.canvas.ReDraw()

  def IncrementPageNumber(self):
    self.current_page_number += 1
    self.ClearAndRedraw()

  def DecrementPageNumber(self):
    self.current_page_number -= 1
    self.ClearAndRedraw()

  def DrawPreviousPageArrow(self):
    """Draw a triangle facing left hooked to decrementing the page number."""
    x1, y1 = self.CanvasCoordinates(0, 10)
    x2, y2 = self.CanvasCoordinates(15, 0)
    x3, y3 = self.CanvasCoordinates(15, 20)
    id = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3)
    self.canvas.tag_bind(id, '<1>', lambda e: self.DecrementPageNumber())

  def DrawNextPageArrow(self):
    """Draw a triangle facing left hooked to incrementing the page number."""
    width = self.width
    x1, y1 = self.CanvasCoordinates(width, 10)
    x2, y2 = self.CanvasCoordinates(width - 15, 0)
    x3, y3 = self.CanvasCoordinates(width - 15, 20)
    id = self.canvas.create_polygon(x1, y1, x2, y2, x3, y3)
    self.canvas.tag_bind(id, '<1>', lambda e: self.IncrementPageNumber())


  def ReDrawView(self, controller):
    items, top_message = self.GetAllItemsToDisplay(controller)
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
    self.canvas.create_text(x, y, text=top_message, anchor=NW)

    row_top_y = 20
    for item in items_to_show:
      self.DrawItem(20, row_top_y, item)
      row_top_y += self.height_per_row

    if self.current_page_number > 1:
      self.DrawPreviousPageArrow()

    if self.current_page_number < max_page_number:
      self.DrawNextPageArrow()
