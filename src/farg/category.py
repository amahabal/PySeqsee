"""Base class for a category."""

from farg.exceptions import FargError

class CategorizableMixin(object):
  """Base class for things which can belong to categories."""
  def __init__(self):
    self.categories = {}

  def AddCategory(self, category, binding):
    """Add a category (with the specified binding) to the object."""
    self.categories[category] = binding

  def RemoveCategory(self, category):
    """Removes the category: the item will not (currently) be considered a member of that category."""
    self.categories.pop(category)

  def GetBindingsForCategory(self, category):
    """Gets bindings. If not an instance of category, raises an exception."""
    return self.categories[category]

  def IsKnownAsInstanceOf(self, category):
    """True if known to be an instance of category."""
    return self.categories.has_key(category)



class Category(object):

  @staticmethod
  def IsInstance(self, object):
    """Is object an instance of this category?
    
    If it is not, `None` is returned. If it is, a binding object is returned.
    """
    raise FargError("IsInstance makes no sense on base category.")

  def FindMapping(self, categorizable1, categorizable2):
    """Finds a mapping between two objects based on a particular category.
    
     .. ToDo:: This is incomplete, since I have not fleshed out mappings yet.
    """
    if not categorizable1.IsKnownAsInstanceOf(self): return None
    if not categorizable2.IsKnownAsInstanceOf(self): return None
