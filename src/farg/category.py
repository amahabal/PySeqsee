"""Classes to deal with categories and their instances, including the base class for
categories.

An example will help describe all that happens here. We will use the category 'Ascending'
from Seqsee. Instances of this category are objects such as '(1 2 3)' and '(7 8 9 10)'.
Objects need to have CategorizableMixin in their class hierarchy: it provides methods to
store the discovered categories and their bindings.

A category is a class (deriving from Category).

Adding a category to an instance::

  bindings = item.DescribeAs(category)

The following also returns a binding, but does not store the membership information::

  bindings = category.IsInstance(item)

"""

from farg.exceptions import FargError

class Binding(object):
  """Specification of how an instance is a member of some category.
  
  .. Note::
  
    In the Perl version, the bindings had special slots for squinting, position, metotype
    etc. Here, all are part of the same hash, along with "regular" attributes such as length.
  
    This also means that the caller of the constructor needs to do all the work, unlike in
    Perl, where some bits were calculated by the constructor. 
  """
  def __init__(self, **bindings):
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


class Category(object):
  """The base class of any category in the FARG system.
  
  Any derivative class must define the following class methods:
  
  * IsInstance (which would return a binding),
  * FindMapping (given two categorizables, returns a mapping between the two)
  * ApplyMapping (given a mapping and a categorizable, returns a new item). 
  """
  @classmethod
  def IsInstance(cls, object):
    """Is object an instance of this category?
    
    If it is not, `None` is returned. If it is, a binding object is returned.
    """
    raise FargError("IsInstance makes no sense on base category.")

  @classmethod
  def FindMapping(cls, categorizable1, categorizable2):
    """Finds a mapping between two objects based on a particular category."""
    raise FargError("IsInstance makes no sense on base category.")

  @classmethod
  def ApplyMapping(cls, categorizable, mapping):
    """Apply a mapping to a categorizable to obtain a different categorizable."""
    raise FargError("IsInstance makes no sense on base category.")
