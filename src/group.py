import numbers
from item import Item
from integer import Integer

class Group(Item):
  def __init__(self, *items):
    self.items = items
    subobjects = list(self._subobjects())
    if len(set(subobjects)) != len(subobjects):
      raise Exception("Repeated object")

    
  def __getitem__(self, index):
    return self.items[index]

  @staticmethod  
  def QuickCreate(*items):
    created_items = []
    for item in items:
      if isinstance(item, numbers.Integral):
        created_items.append(Integer(item))
      else:
        created_items.append(Group.QuickCreate(*item))
    return Group(*created_items)
    
  def size(self):
    return len(self.items)
  
  def _subobjects(self):
    yield self
    for item in self.items:
      for subobject in item._subobjects():
        yield subobject
