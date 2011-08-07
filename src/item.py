from category_manager import CategoryManager
class Item:
  def __init__(self):
    self.cm = CategoryManager()

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
  