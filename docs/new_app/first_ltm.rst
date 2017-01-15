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

The subtleties of storing
---------------------------

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
solution used here/

We will return to these issues below on this page.

Managing several LTMs
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
