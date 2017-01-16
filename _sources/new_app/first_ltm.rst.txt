Long-term memory
==================

We continue our foray into the mechanics of doing things in PySeqsee while temporarily setting aside
cognitive considerations. We will take a look at the long-term memory.

The graph
-----------

The long-term memory in PySeqsee is a graph, whose nodes are individual concepts. There is no
restriction on what the concepts may be---anything implementing a particular interface
(:py:class:`~farg.core.ltm.storable.LTMStorableMixin`) is welcome.

All categories, being instances of :py:class:`~farg.core.categorization.category.Category`, subclass
from the LTMStorableMixin, and are therefore ready to be stored in the graph.

Preparing a class to be storable
-----------------------------------

Subclassing from LTMStorableMixin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We will begin by creating a class to hold integers that we will be storing in the LTM. We will put
this class in farg/apps/bongard/workspace.py, where we also have IntegerObject, which stores each
item in the input. ::

  from farg.core.ltm.storable import LTMStorableMixin
  from farg.core.meta import MemoizedConstructor

  class PlatonicInteger(LTMStorableMixin, metaclass=MemoizedConstructor):
    """Integer in long-term memory.

    Holds an integer that can be stored in LTM (and about which we can store information such as
    remembered categories."""

    def __init__(self, magnitude):
      self.magnitude = magnitude

A fair question to ask is why we do not just reuse IntegerObject for this purpose. The answer is twofold.
First, the two are conceptually different and will hold different pieces of information. The version
used for LTM (i.e., PlatonicInteger) will store what has been remembered about an integer from prior runs, whereas the
the version for storing in the workspace (i.e., IntegerObject) will hold what has been seen in the
current run and information about similarities to objects seen in this problem. Second, we want a
single integer "3" in the long term memory, but multiple copies of "3" may be needed in the workspace
since we may not only have "3" explicitly in the input, it may sneak in in other places, as would
happen if one side is made up of cubic numbers such as 1, 8, and 27 and we see these as the third powers.

The metaclass :py:class:`~farg.core.meta.MemoizedConstructor` ensures that repeated calls to
the constructor of PlatonicInteger return the same object.

Associating LTM objects with workspace objects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

But we still need to relate IntegerObject instances to PlatonicInteger objects. That is, when we
see a "3" in the input, we need a way to connect to the "3" in the LTM. We do this by subclassing
IntegerObject from LTMStorableMixin, but defining the GetLTMStorableContent method to return a
platonic integer::

  class IntegerObject(CategorizableMixin, LTMStorableMixin):
    """Holds one item in either set, along with any book-keeping information."""
    
    def __init__(self, magnitude):
      self.magnitude = magnitude

    def GetLTMStorableContent(self):
      return PlatonicInteger(self.magnitude)

Accessing the nodes in the graph
----------------------------------

Given an LTM graph, we can get the nodes associated with some content (i.e., an instance of LTMStorableContent)
thus::

  # graph holds the graph.
  # i7 holds IntegerObject(7), and pi7 holds a PlatonicInteger(7)
  node = graph.GetNodeForContent(i7)
  node2 = graph.GetNodeForContent(pi7)
  # node == node2
  
.. TODO:
  Describe activations, adding activation, adding edges between nodes and accessing these. This
  could be described elsewhere and pointed to from here.


Subtleties not yet touched here
-----------------------------------

We have not yet described what the method LTMDepenedentContent of LTMStorableMixin does. It is
concerned with storing complex nodes whose definition depends upon other nodes.

.. sidebar:: Why is this so complex?
  :subtitle: The subtleties of storing

  The range of pitfalls in implementing a long-term memory are many, and I will illustrate this with
  an example. Consider wanting to store the category "Even squares", which has been defined, let us say,
  as the intersection of the categories "Even" and "Square".
  
  We would like to be able to store this category in the graph and dump the ltm into a file. Without
  the storage to a file, we are restricted to the life span of a single run, and this can hardly be termed
  "long". In a subsequent run, we would also like to resuscitate the category (why else would one store
  it otherwise?)
  
  But our category is defined in terms of two other categories, and we would need to store these as
  well. All dependencies of a node that is stored also themselves need to be stored.
  
  The Python standard module :py:mod:`pickle` is intended for use in such cases, and it is part of the
  solution used here.


Management of LTMs
-----------------------

Instead of having a giant graph of all nodes, PySeqsee has opted for one LTM per subspace (a subspace
is related to the notion of a mental space from cognitive science). Each such LTM has a name, and an
:py:class:`~farg.core.ltm.manager.LTMManager` manages these. A single instance of a manager is active
at a time.

.. TODO::

  Write about when and where this is set up.

Registering an LTM initializer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

LTMManager keeps track of names of managers. At startup, it lazily loads the LTMs in a particular directory.
If an LTM file is missing or empty, it can be seeded with some initial nodes if an initializer has been
registered. Such an initializer is a function that populates an LTM.

GetLTM(name)
^^^^^^^^^^^^^^

This method returns an LTM if it has already been loaded. If it has not yet been loaded, it attempts
to read the appropriate file from disk. If that too fails, but an initializer has been specified,
that is now run. In the absence of an initializer, an empty graph is returned.

SaveAllOpenLTMs()
^^^^^^^^^^^^^^^^^^

As the name suggests, this saves all the open LTMS.
