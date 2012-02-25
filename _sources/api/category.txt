Category
===========

This is the root of all categories.

  * Provides a method to check if an entity is an instance. Returns a binding --- a
    description of how this is an instance. For example, the binding for the category
    Mountain for the entity "5 6 7 8 7 6 5" might be that 8 is the peak and 5 the base::
    
      binding = IsInstance(entity)

CategorizableMixin
=====================

Any entity that we wish to be an instance of a category must derive from this mixin.

  * Allows access to categories of which this is a known instance. This is a dict keyed
    by category and containing bindings for values::
    
      self.categories

  * It provides the ability to add and remove categories. Removing a non-existant category
    is not an error::
    
      self.AddCategory(category, binding)
      self.RemoveCategory(category)
      
  * You can get bindings or check whether this is known to be an instance of a category. For
    getting binding, it is an error to call this with a category this is not an instance of::
    
      self.IsKnownAsInstanceOf(category)
      binding = self.GetBinding(category)
      
  * The following checks if an entity is a known instance of a category, and if not, uses the
    category to describe this object as an instance::
    
      binding = self.DescribeAsInstanceOf(category)
      
Binding
=========

  * To construct a binding, use a dict::
  
     b = Binding(dict(base=7, peak=9))
    
  * And you can get the binding for any attribute::
  
     v = GetBindingForAttribute('peak')
    
  * The entire binding is also available to iterate over::
  
     self.binding 