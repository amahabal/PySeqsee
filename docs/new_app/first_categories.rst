First Categories
===================

Categories are the stars in the Bongard domain: what we are trying to find is a category that has
all items on the left as members and none of the items on the right as members. On this page, we
will take our first steps by defining a category---Squares---and a family of categories---Modulo.

The focus is still on the mechanics of how to do this, and subsequently we will delve deeper into
cognitive considerations.

Categories, Categorizable, and Bindings
------------------------------------------

We need to get some notation out of the way. When I say *category* on this page, I am referring to
such things as the category "even number", "prime number", and to take two examples not from this
domain, "chairs" and "common first name". For now, this can be thought of as a set of items with
degrees of membership (but much more will be said later).

By a *categorizable*, I mean a Python object that has the necessary routines to keep track of
categories. This can be achieved by subclassing from the interface
:py:class:`~farg.core.categorization.categorizable.CategorizableMixin`.

Finally, a binding can be thought of as an explanation for how an item is an instance of a category.
For instance, one may explain that "16" is a square by saying that the square root is 4. This can
open the possibility of seeing how "16" is related to "25 by using the relationships between the
bindings. Formally, a binding is an instance of 
:py:class:`~farg.core.categorization.binding.Binding`.

Turning IntegerObject into a Categorizable
--------------------------------------------

In farg/apps/bongard/workspace.py, let's turn IntegerObject into a categorizable. To do this, we
need to add a super-class. No extra methods are needed. ::

  from farg.core.categorization.categorizable import CategorizableMixin

  class IntegerObject(CategorizableMixin):
    # Existing stuff.

Adding the category "Square"
------------------------------

The file farg/apps/bongard/categories.py already exists, and we will add the new category to this.
Our category must inherit from :py:class:`~farg.core.categorization.category.Category`, and it should
define the method IsInstance that would return a Binding object. ::

  class Square(Category):
    """Category whose instances are IntegerObject that are square numbers."""

    def BriefLabel(self):
      return "Square"

    def IsInstance(self, entity):
      magnitude = entity.magnitude
      if magnitude < 0:
        return None  # Not an instance.
      root = math.sqrt(magnitude)
      if root != int(root):
        return None
      return Binding(sqroot=root)

What can we do with this?
---------------------------

What does this enable us to do? Here is a sampler. ::

  i7 = IntegerObject(7)
  i9 = IntegerObject(9)
  sq = Square()
  b = i7.DescribeAs(sq)  # b will be None
  b = i9.DescribeAs(sq)  # b won't be none.
  b = i9.DescribeAs(sq)  # No recalculation: i9 can remember its categories.
  i9.IsKnownAsInstanceOf(sq)
  b = i9.GetBindingsForCategory(sq)  # Requires it to be a known instance


