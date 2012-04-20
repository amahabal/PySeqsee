# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

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
    return category in self.categories

  def DescribeAs(self, category):
    """Describes item as instance of category, and remembers the binding if one is found.
    
    Returns the binding.
    """
    if category in self.categories:
      return self.categories[category]
    binding = category.IsInstance(self)
    if binding:
      self.categories[category] = binding
      return binding
    return None

  def GetCommonCategoriesSet(self, other):
    """Returns a list of discovered categories common to this and the other categorizable."""
    return set(self.categories.keys()).intersection(list(other.categories.keys()))

  def AddCategoriesFrom(self, other):
    """Copy categories in 'other' to 'self'"""
    my_categories = self.categories
    for cat, binding in other.categories.items():
      if not cat in my_categories:
        my_categories[cat] = binding
