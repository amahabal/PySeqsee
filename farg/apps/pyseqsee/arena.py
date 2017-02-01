"""An arena is a sequence of elements with possibly overlapping groups.

It is one of the core pieces of the workspace, but may be used elsewhere."""
from farg.apps.pyseqsee.objects import PSElement

class PSArena(object):

  def __init__(self, *, magnitudes, start=0):
    self.element = []
    self._start = start
    self._next_index = start
    self.Append(magnitudes=magnitudes)

  def Size(self):
    return len(self.element)

  def Append(self, *, magnitudes):
    to_add = [PSElement(magnitude=x) for x in magnitudes]
    for idx, el in enumerate(to_add, self._next_index):
      el._span = (idx, idx)
    self.element.extend(to_add)
    self._next_index += len(magnitudes)

  def CheckTerms(self, *, start, magnitudes):
    for offset, mag in enumerate(magnitudes, start):
      idx = offset - self._start
      assert(idx >= 0)
      assert(idx < len(self.element))  # TODO: This should raise a specific Exception
      if self.element[idx].magnitude != mag:
        return False
    return True
