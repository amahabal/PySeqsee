"""An arena is a sequence of elements with possibly overlapping groups.

It is one of the core pieces of the workspace, but may be used elsewhere."""
from farg.apps.pyseqsee.objects import PSElement

class ElementBeyondKnownSoughtException(Exception):
  pass

class PSArena(object):

  def __init__(self, *, magnitudes, start=0):
    #: List of elements, each is a PSElement
    self.element = []
    #: Offset of the first element, which will normally be 0.
    self._start = start
    #: Index at which to insert next element.
    self._next_index = start
    self.Append(magnitudes=magnitudes)

  def Size(self):
    """Number of elements in the arena."""
    return len(self.element)

  def Append(self, *, magnitudes):
    """Adds elements with these magnitudes at the end."""
    to_add = [PSElement(magnitude=x) for x in magnitudes]
    for idx, el in enumerate(to_add, self._next_index):
      el._span = (idx, idx)
    self.element.extend(to_add)
    self._next_index += len(magnitudes)

  def CheckTerms(self, *, start, magnitudes):
    for offset, mag in enumerate(magnitudes, start):
      if offset >= self._next_index or offset < self._start:
        raise ElementBeyondKnownSoughtException()
      idx = offset - self._start
      if self.element[idx].magnitude != mag:
        return False
    return True
