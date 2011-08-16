from category_manager import CategoryManager
class Item:
  def __init__(self):
    self.cm = CategoryManager()
    self.related_map = {}

  def SetMetonym(self, other):
    self._metonym = other
  def Metonym(self):
    return self._metonym
  def HasMetonym(self):
    return hasattr(self, '_metonym')
  def TerminalMetonym(self):
    if hasattr(self, '_metonym'):
      return self._metonym.TerminalMetonym()
    else:
      return self

  def DescribeAs(self, category):
    category.CheckIfInstance(self)
    
  def IsRelatedTo(self, other):
    return self.related_map.has_key(other)
  
  def RelationTo(self, other):
    return self.related_map[other]
  
  def OutgoingRelations(self):
    for other, r  in self.related_map.iteritems():
      if r.left == self:
        yield r
  def IncomingRelations(self):
    for other, r  in self.related_map.iteritems():
      if r.right == self:
        yield r
  def Relations(self):
    return self.related_map.values()
  