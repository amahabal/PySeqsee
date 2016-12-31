Adding Categories
===================

Categories will play a starring role in reaching a solution for a numeric bongard
problem. We want to be able to describe a number as any of the following, just to
pick a few examples:

* Prime
* Composite
* Odd
* Even
* Not a prime (e.g., 1)
* Triangular (i.e, n(n+1)/2 for some n)
* Square
* Power of 2
* "Small" 
* 3 mod 4
* Positive

To this end, we will make Element an instance of Categorizable. Specifically, in
the file workspace.py we will change the class to become::

  from farg.core.categorization.categorizable import CategorizableMixin

  class Element(CategorizableMixin):
    """Class to store individual elements of the left and right sets."""
    def __init__(self, magnitude):
      self.magnitude = magnitude

This allows us later to mark elements as belonging to specific categories. The
syntax for doing so is described by this snippet::

  element = Element(7)
  # Assume that we have defined a category 'Prime' somewhere (described below).

  # This adds a category. 'how' explains how this is a category. In Seqsee, the
  # 'how' for an ascending group includes the start and end element. For prime,
  # for this application, it could be empty.
  element.AddCategory(Prime, how)  # 'how' is described below

  # This call attempts to describe the element as being a prime. It will call the
  # IsInstance method of the category.
  element.DescribeAs(Prime)
  
  # The following is true or false:
  element.IsKnownInstanceOf(Prime)



