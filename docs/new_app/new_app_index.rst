Creating a new app
====================

.. warning::

  Under active updating (as of Jan 8, 2017)

This section will describe the process of creating a full new application. It will
attempt to touch all aspects of the process.

The application developed in this tutorial may be called "Numeric Bongard". A "Bongard problem"
consists of two sets of items---left and right---and the goal is to spot a rule that applies to all
items in one set but none in the other.

Here is an example. If one set contains the numbers 3, 7, and 11, and the other set contains 9, 15,
and 21, then a correct "solution" is to say that the first set contains primes and the second set
contains the composite numbers. Another example, more complex, includes items such as 3, 7, and 11 on
one side and 2, 5, 13, 17 and 15 on the other. Here, one answer may be "the left hand set contains
items that are primes of the form 3 mod 4", and the other side contains all other numbers.

One smart alecky answer can always be "the left hand side contains exactly those numbers and none other",
but that would be missing the point that for many problems there are simpler and more elegant answers
that people effortlessly spot.

Complexity of the domain
--------------------------

The complexity of a slightly spiced up version of the domain is horrendous. If the two sides, instead
of being sets of numbers, are sets of tuples (an example of a tuple is "2 3 4" and another is
"6 1 6"), then one can create problems that are easy for people but quite hard for computers.

As an illustration, consider this::

  Set 1:
    1 1 2 2 3 3
    12 12 13 13 14 14 15 15
  
  Set 2:
    8 9 10 11
    8 8 8 9 9 9 10 10 10


For our current purposes, we will stick to using numbers, merely any of these ideas could of
course be sneaked into that domain as well.

The Bongard domain is a great place to use FARG concepts.  In this situation, there is no "right"
answer, all that matters is that an answer can be given with an intelligent reason.  Because of this,
using a typical brute force pattern finder would not capture the fluidity of the problem.  Using FARG
concepts like the parallel terraced scan embrace the open-ended nature of the problem.

Creating the app's skeleton
--------------------------------

In this phase, we will set up the initial skeleton of the app and get it to a useful point where we
can have some fun.

.. toctree::
   :maxdepth: 1

   create_new_app
   add_input_flags
   update_workspace
   update_gui

First Codelets
------------------

In this phase, we will lay a bit more groundwork. We will make our first codelet, and "solve" our
first Bongard problem. However, this shall be done in a cognitively implausible way: the goal is to
demonstrate the pieces, and we will put these to better use in the coming phases.

.. toctree::
   :maxdepth: 1

   first_codelet
   first_categories
   focusing

