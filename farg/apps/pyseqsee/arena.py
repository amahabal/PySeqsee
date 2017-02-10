"""An arena is a sequence of elements with possibly overlapping groups.

It is one of the core pieces of the workspace, but may be used elsewhere."""
from farg.apps.pyseqsee.objects import PSElement, PSGroup
from _collections import defaultdict

class ElementBeyondKnownSoughtException(Exception):
  pass

class CannotInsertGroupWithoutSpans(Exception):
  pass

class PSArena(object):

  def __init__(self, *, magnitudes, start=0):
    #: List of elements, each is a PSElement
    self.element = []
    #: Offset of the first element, which will normally be 0.
    self._start = start
    #: Index at which to insert next element.
    self._next_index = start
    #: Objects at span. Multiple values are possible at a span; for instance, at position 3, we may
    #: have the element 3 and the singleton gp 3, as well as the singleton gp containing singleton
    #: group. Given a span and a structure, however, the object is unique, and this is how things
    #: are stored, keyed by the structure.
    self._objects_with_span = defaultdict(dict)
    self.Append(magnitudes=magnitudes)

  def Size(self):
    """Number of elements in the arena."""
    return len(self.element)

  def Append(self, *, magnitudes):
    """Adds elements with these magnitudes at the end."""
    to_add = [PSElement(magnitude=x) for x in magnitudes]
    for idx, el in enumerate(to_add, self._next_index):
      el._span = (idx, idx)
      self._objects_with_span[(idx, idx)][el.Structure()] = el
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

  def GetObjectsWithSpan(self, span):
    """Given a span, returns a dict mapping structure to objects."""
    return self._objects_with_span[span]

  def _MergeObjectDetails(self, other_obj, obj_in_arena):
    obj_in_arena.MergeCategoriesFrom(other_obj)

  def MergeObject(self, obj):
    span = obj.Span()
    if not span:
      raise CannotInsertGroupWithoutSpans()
    # TODO(amahabal): Check CheckTerms() returns true...
    if isinstance(obj, PSElement):
      element_here = self.element[span[0] - self._start]
      self._MergeObjectDetails(obj, element_here)
      return element_here
    parts = [self.MergeObject(x) for x in obj.items]
    obj_structure = obj.Structure()
    objects_at_location = self.GetObjectsWithSpan(span)

    obj_structure = obj.Structure()
    if obj_structure in objects_at_location:
      obj_in_arena = objects_at_location[obj_structure]
    else:
      obj_in_arena = PSGroup(items=parts)
      self._objects_with_span[span][obj_structure] = obj_in_arena
      obj_in_arena.InferSpans()
    self._MergeObjectDetails(obj, obj_in_arena)
    return obj_in_arena

