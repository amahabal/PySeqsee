from item import Item
class Integer(Item):
  """
  Represents a single numeric entity (e.g., one element of a group, or a length)
  """

  def __init__(self, magnitude):
    self.magnitude = magnitude
    
  def _subobjects(self):
    yield self