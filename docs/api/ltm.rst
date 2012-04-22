Long-term Memory
===================

Long-term memory in Farg consists of multiple graphs, one per type of subspace.
Each graph contains nodes (for example, nodes for categories, mappings,
individual numbers, or whatever else) and edges (that connect nodes, and have
types).

Activations
-------------

With each node is associated a number between 0 and 1 called its activation. The
activation can be considered as the level of belief that the concept is relevant
to the problem at hand.

As evidence mounts for a node's relevance, its activation climbs. This is
sigmoidal. That is, the activation initially climbs very slowly as evidence
mounts --- that is, a small amount of evidence leads to near-zero activation. The
following chart (whose x-axis will be explained momentarily) illustrates this:

.. raw:: html

  <img src="http://chart.apis.google.com/chart?chxr=0,0,1&chxt=y,x&chs=440x220&cht=lxy&chco=3072F3&chds=0,100,0,1&chd=t:0,10,20,30,40,50,60,70,80,90,100|0.003,0.018,0.043,0.093,0.22,0.562,0.811,0.895,0.932,0.952,0.964&chdl=Activation&chdlp=b&chls=2,4,1&chma=5,5,5,25&chtt=Activation+given+evidence" width="440" height="220" alt="Activation given evidence" />

Evidence Space
----------------

Although the activation of the node is an important number, PySeqsee does all its
calculations in another space, the evidence space (which is what the x-axis in the
chart above represents). A codelet may add activation to a node, but this is specified in
evidence space. Relevant method::

  node.AddActivation(10) # This'd change activation from 0.22 to 0.56, or from
                         # 0.003 to 0.018.

Decay
------

Activation decays over time. To ease calculations, the LTM keeps track of the
number of timesteps elapsed. This is available thus::

  ltm._timesteps

When the activation of a node is requested, its activation is decreased appropriately.
It thus needs to keep track of when last a node's activation was calculated::

  node._time_of_activation_update
  node.GetActivation()  # Decays as appropriate and updates _time_of_activation_update

Activation spread
------------------

What can be a node
--------------------

Types of edges
----------------

The LTM is "active"
--------------------

API
-------

* To construct, a filename is passed in. If missing, an empty graph will be created::

    graph = LTMGraph("foo.ltm")

* To check emptiness::

    self.IsEmpty()

* To save to the specified file (and a no-op if no file specified)::

    self.Save()

* To retrieve a node or add when non-existent::

    node = self.GetNodeForContent(content)

* Activation of the node can be increased::

    self.SpikeNodeForContent(content, amount)