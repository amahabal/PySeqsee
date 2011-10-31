"""A relation is a specific instance of a mapping."""

class Relation(object):
  def __init__(self, first, second, mapping):
    #: The object on the left.
    self.first = first
    #: The object on the right.
    self.second = second
    #: The mapping to transform the left object to the right object.
    self.mapping = mapping

  def Ends(self):
    """Returns a 2-tuple of the two ends."""
    return (self.first, self.second)

  def AreEndsContiguous(self):
    """Are the two ends right next to each other (i.e., true if no hole)."""
    return self.first.end_pos + 1 == self.second.start_pos



