"""Base class for a category."""

from farg.exceptions import FargError

class Binding(object):
  """Specification of how an instance is a member of some category.
  
  .. Note::
  
    In the Perl version, the bindings had special slots for squinting, position, metotype etc. Here,
    all are part of the same hash, along with "regular" attributes such as length.
  
    This also means that the caller of the constructor needs to do all the work, unlike in Perl,
    where some bits were calculated by the constructor. 
  """
  def __init__(self, bindings):
    self.bindings = dict(bindings)

  def GetBindingsForAttribute(self, attribute_name):
    """Get the binding of a single attribute."""
    return self.bindings[attribute_name]

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

  def DescribeAs(self, category):
    if self.categories.has_key(category):
      return self.categories[category]
    binding = category.IsInstance(self)
    if binding:
      self.categories[category] = binding
      return binding
    return None

class Category(object):

  @classmethod
  def IsInstance(cls, object):
    """Is object an instance of this category?
    
    If it is not, `None` is returned. If it is, a binding object is returned.
    """
    raise FargError("IsInstance makes no sense on base category.")

  @classmethod
  def FindMapping(cls, categorizable1, categorizable2):
    """Finds a mapping between two objects based on a particular category.
    
     .. ToDo:: This is incomplete, since I have not fleshed out mappings yet.
    """
    if not categorizable1.IsKnownAsInstanceOf(cls): return None
    if not categorizable2.IsKnownAsInstanceOf(cls): return None

  def ApplyMapping(cls, categorizable, mapping):
    """Apply a mapping to a categorizable to obtain a different categorizable.
    
     .. ToDo:: This is incomplete, since I have not fleshed out mappings yet.
    """
    if mapping.category is not cls:
      raise FargError("Apply mapping called on wrong category.")
    if not categorizable.IsKnownAsInstanceOf(cls):
      raise FargError("Apply mapping called on wrong object not an instance of category.")
