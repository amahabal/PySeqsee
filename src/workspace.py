from group import Group
from integer import Integer

class Overlay(object):
  def __init__(self, item, start, end):
    self.item = item
    self.start = start
    self.end = end
    
  def Length(self):
    return self.end - self.start

# TODO Move to a util file
def flatten(tup):
  if isinstance(tup, tuple):
    for t in tup:
      for f in flatten(t):
        yield f
  else:
    yield tup

class Workspace(object):
  def __init__(self):
    self.elements = []
    self.overlays = []
    
  def AddElements(self, *ints):
    self.elements.extend(ints)
    
  def ElementsCount(self):
    return len(self.elements)
  
  def AddOverlay(self, item, start, end):
    ov = Overlay(item, start, end)
    #  Error checking?
    self.overlays.append(ov)
    return ov
  
  def AlignsWith(self, item, start):
    structure_to_expect = item.Structure()
    for idx, item in enumerate(flatten(structure_to_expect), start=start):
      if self.elements[idx] != item:
        return False
    return True