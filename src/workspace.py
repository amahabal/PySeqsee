from group import Group
from integer import Integer

def Equals(x):
  """Returns an equality tester."""
  return (lambda(y): x == y)

def GreaterThanEq(x):
  return (lambda(y): y >= x)

def GreaterThan(x):
  return (lambda(y): y > x)

def LessThanEq(x):
  return (lambda(y): y <= x)

def LessThan(x):
  return (lambda(y): y < x)

def Between(x, y):
  return (lambda(z): x <= z and z <= y)

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
  
  def _AddOverlay(self, item, start, end):
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
  
  def GetOverlays(self, left_edge_pred, right_edge_pred, item_pred=None):
    overlays = self.overlays
    if left_edge_pred:
      overlays = [x for x in overlays if left_edge_pred(x.start)]
    if right_edge_pred:
      overlays = [x for x in overlays if right_edge_pred(x.end)]
    if item_pred:
      overlays = [x for x in overlays if item_pred(x)]
    return set(x.item for x in overlays)

  def GetOverlaysOverlapping(self, start, end, item_pred=None):
    set1 = self.GetOverlays(LessThanEq(start), GreaterThan(start), item_pred)
    set1.update(self.GetOverlays(LessThan(end), 
                                 GreaterThanEq(end),
                                 item_pred))
    set1.update(self.GetOverlays(GreaterThanEq(start),
                                 LessThanEq(end),
                                 item_pred))
    return set1