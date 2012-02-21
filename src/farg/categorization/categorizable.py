class CategorizableMixin(object):
  """Base class for things which can belong to categories."""
  def __init__(self):
    self.categories = {}

  def AddCategory(self, category, binding):
    """Add a category (with the specified binding) to the object."""
    self.categories[category] = binding

  def RemoveCategory(self, category):
    """Removes the category: the item will not (currently) be considered a member of that
       category.
    """
    self.categories.pop(category)

  def GetBindingsForCategory(self, category):
    """Gets bindings. If not an instance of category, raises an exception."""
    return self.categories[category]

  def IsKnownAsInstanceOf(self, category):
    """True if known to be an instance of category."""
    return self.categories.has_key(category)

  def DescribeAs(self, category):
    """Describes item as instance of category, and remembers the binding if one is found.
    
    Returns the binding.
    """
    if self.categories.has_key(category):
      return self.categories[category]
    binding = category.IsInstance(self)
    if binding:
      self.categories[category] = binding
      return binding
    return None

  def GetCommonCategoriesSet(self, other):
    """Returns a list of discovered categories common to this and the other categorizable."""
    return set(self.categories.keys()).intersection(other.categories.keys())

