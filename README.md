#PySeqsee
A python framework for solving complex problems not amenable to brute force.

PySeqsee aims to be a robust framework for developing blackboard-architecture
based programs that tackle hard problems in a human-like way.

It is open-source, under GNU GPLv3.

###Links

Mailing List:
  - https://groups.google.com/forum/#!forum/pyseqsee (to view)
  - pyseqsee@googlegroups.com (to post)

Documentation: http://amahabal.github.com/PySeqsee/
Source Code: https://github.com/amahabal/PySeqsee
Bug Tracker: https://github.com/amahabal/PySeqsee/issues
Development Status: Alpha, but actively-developed working code

###Brief history and motivation

For over two decades now, Douglas Hofstadter's Fluid Analogies Research
Group at Indiana University has designed computer simulations aimed
at understanding human cognition.  Each successive model has usually been
written from scratch.  Very little of the actual code from previous
implementations was used by subsequent implementations, although ideas
and the basic approach survived.

Not just were the implementations different, they were typically in
different languages.  Franz Lisp, Chez Scheme, C++, Perl have
been used by various projects, and even Delphi was used in Capyblanca.  A Java
port of Copycat exists.

This project aims to create a framework in which to implement various
cognitive architectures.  It is written in Python 3, and aims to provide
many components out of the box without making too many irreversible
commitments.  That is, it provides a full suite of tools to get the job
done, but also allows you to swap out any component and use the rest.

###Services provided (and their level of completion):

* A reusable GUI. Every project will have a different workspace, but there is
  still much that is shared. PySeqsee allows you to just write the visualization
  for your data, and takes care of everything else. (complete)
* A robust testing framework. If you wish to test how well a proposed new feature
  works, you can run a side-by-side comparison over many inputs and see the stats.
  All that is needed is a file with the inputs to test and in case the input is
  very specialized, a python class to convert these inputs to flags to be passed in.
  (status: functionality implemented, but statistical analysis to compare which
   of the two sides is better is not done).
* A setup script that creates the skeleton of a new project. (Under development,
  basic functionality exists).
* A coderack and facilities for writing codelets (complete).
* A slipnet (known here as Long-term Memory), along with the ability to add nodes
  and edges and the ability to save it to disk (works, but could be significantly
  improved).
* A stream of thought. This is a component that first appeared in Seqsee (written
  in Perl), but plays a central role here. The stream provides a temporal context
  --- that is, recent thoughts can influence what the system does in flexible ways.
  A full implementation exists.
* A full reimplementation of Seqsee (status: under development. Many sequences
  seen, but not all that the perl version did). A short video of the Perl version
  can be found here: http://www.youtube.com/watch?v=2KWtRUg8kL8. The dissertation
  is here: http://www.amahabal.com/files/Seqsee--doublesided.pdf
