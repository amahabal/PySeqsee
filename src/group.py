import numbers
from integer import Integer

class Group(object):
  def __init__(self, *items):
    self.items = items

  @staticmethod  
  def QuickCreate(*items):
    created_items = []
    for item in items:
      if isinstance(item, numbers.Integral):
        created_items.append(Integer(item))
      else:
        created_items.append(Group.QuickCreate(*item))
    return Group(*created_items)
    
  def __getitem__(self, index):
    return self.items[index]
    
  def size(self):
    return len(self.items)