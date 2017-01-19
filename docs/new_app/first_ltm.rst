Long-term memory
==================

We continue our foray into the mechanics of doing things in PySeqsee while temporarily setting aside
cognitive considerations. We will take a look at the long-term memory.

Remembering between runs
--------------------------

When an app runs on some input, it may figure something out in the process of solving it. It can
store this information in its long-term memory, which is written out to disk. On a different run,
this piece of information may come in handy.

Here is an example of what may happen. Suppose that the Bongard app knows the category Square, and
can answer the question "Is this a square", and knows a few squares such as 1, 4, and 9, but that
it does not know 121 to be a square. It sees a problem where the left-hand side contains 1, 9, and
121, and it asks itself the question "Is 121 a square?" and then remembers the fact that it is.
Later, when it encounters another problem with a "121", it may "remember" that that is a square.

The memory is stored as a graph, as described below.

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

    def BriefLabel(self):
      return 'Platonic %d' % self.magnitude

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

Initializing the graph
------------------------

When the application is run multiple times and sees a range of input problems, the long-term memory
gradually becomes richer. But even at the beginning, it is useful to start off with at least a few
elements, and this is achieved by an initializer.

The LTM Manager
^^^^^^^^^^^^^^^^^
Instead of having a giant graph of all nodes, PySeqsee has opted for one LTM per subspace (a subspace
is related to the notion of a mental space from cognitive science). Each such LTM has a name, and an
:py:class:`~farg.core.ltm.manager.LTMManager` manages these.

It loads graphs from disk on demand, when GetLTM(name) is called. That call loads the file if it has
not already been loaded. If the file does not exist, but an initializer has been defined, then that
is called to set up the initial nodes.

Initial setup for Bongard
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When the app skeleton was created, hooks for initializing the LTM were already in place, in the file
farg/apps/bongard/controller.py::

  kLTMName = 'bongard.main'
  
  def InitializeBongardLTM(ltm):
    """Called if ltm was empty (had no nodes)."""
    pass

  LTMManager.RegisterInitializer(kLTMName, InitializeBongardLTM)

Let's add some nodes to that graph, and a few edges. We will add nodes corresponding to the integers
0 through 9, a node for the category "Square", and edges between four of those nodes and this
category node. That edge will be marked as connecting instance to category::

  def InitializeBongardLTM(ltm):
    """Called if ltm was empty (had no nodes)."""
    for i in range(10):
      ltm.GetNodeForContent(PlatonicInteger(i))
    for i in (0, 4, 9):
      ltm.AddEdgeBetweenContent(PlatonicInteger(i), Square(),
                                LTMEdge.LTM_EDGE_TYPE_ISA)

When the app is run
^^^^^^^^^^^^^^^^^^^^

When the app is run (via the "farg run bongard" command), a file will show up in the persistent
directory (which, by default, is the directory .pyseqsee in your home directory but can be changed
via the persistent_directory flag---see farg_flags.py). By default, then, you should expect to see
a file at ~/.pyseqsee/bongard/ltm/bongard.main.

To see the content of this LTM, use this::

  farg ltm bongard bongard.main
