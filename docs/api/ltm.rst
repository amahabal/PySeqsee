Long-term Memory
===================

LTM in Farg consists of multiple graphs, one per type of subspace.

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