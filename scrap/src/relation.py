class Relation(object):
  
  def __init__(self, left, right, mapping):
    self.left = left
    self.right = right
    self.mapping = mapping
    
  def ConflictsExisting(self):
    left_relations_map = self.left.related_map
    if self.right not in left_relations_map:
      return False
    if left_relations_map[self.right] == self:
      return False
    return True
  
  def Insert(self):
    if self.ConflictsExisting():
      raise Exception("Cannot insert conflicting")
    self.left.related_map[self.right] = self
    self.right.related_map[self.left] = self

  def Uninsert(self):
    self.left.related_map.__delitem__(self.right)
    self.right.related_map.__delitem__(self.left)