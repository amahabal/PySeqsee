How to install PySeqsee
=========================

Requirements
---------------

* Python 3.1 or higher. You can download this from http://python.org if you don't already
  have it (most Linux systems should already have this installed, probably
  at `/usr/bin/python3`). 

On Linux (or other Unix-like system)
----------------------------------------

Change to the directory where you want to put PySeqsee and type::

  git clone https://github.com/amahabal/PySeqsee.git

This will create a directory called PySeqsee. To test that everything works,
you can type::

  cd PySeqsee
  /usr/bin/python3 farg/apps/seqsee/run_seqsee.py --sequence="2 3 5 7 11"

On Windows
--------------

You can install ActivePython (available from http://www.activestate.com/activepython/downloads).
Remember to get Python 3 (the default at the top is Python 2). You might need to
install git (see http://help.github.com/win-set-up-git/ You only need to install it,
no need to bother with ssh setup or whatnot, unless you want to upload code yourself).

You will then use git to fetch https://github.com/amahabal/PySeqsee.git.

Diagnosing issues:
-------------------

If you see an error message that ends with::

  class Subspace(metaclass=SubspaceMeta):
                           ^
  SyntaxError: invalid syntax

The likely reason is that you used Python 2 instead of Python 3.

If you get a message about being unable to load some module, check your
PYTHONPATH. On Linux, you may need to run::

  export PYTHONPATH=".:$PYTHONPATH"

If something goes wrong
-------------------------

Please email pyseqsee@googlegroups.com
