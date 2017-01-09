Running a set of examples in batch
=======================================

To illustrate running a set of examples as a batch, I will again use the example of Seqsee.

Command
---------

The following line will run Seqsee on a handful of sequences 10 times each::

  python3 -m farg.apps.seqsee.run_seqsee --run_mode=batch --input_spec_file=farg/apps/seqsee/testing_sequences.txt


What is displayed
--------------------

A two pane window is generated, the left hand side of which are examples. Selecting any displays the
relevant statistics on the right hand side: how many times has the sequence been run, success rate,
a histogram showing time taken for each run, and mean and median of the time taken.

Also shown are the statistics from the most recent prior run, if any.


Specifying examples to run
-----------------------------

The file containing the examples can be pointed to by the flag --input_spec_file. The Seqsee app
contains one such file (farg/apps/seqsee/testing_sequences.txt), containing lines such as::

  2 3 5 7|11 13 17
  1 2 3 4 5 6 7 8 9 10 | 11 12 13 14 15
  1 2 1 2 3 1 2 3 4|1 2 3 4 5 1 2 3 4 

which specify the input and the continuation. How such a file is interpreted is up to the app, which
must provide a subclass of 'ReadInputSpec' that can convert a single line of the file into arguments
that may be passed in to the application. This subclass in the case of Seqsee converts the first
line shown above to the sequence [--sequence 2 3 5 7 --continuation 11 13 17].

Other flags
-------------

--num_iterations
^^^^^^^^^^^^^^^^^^

How many times to run each sequence. Defaults to 10.

--max_steps
^^^^^^^^^^^^^

Maximum number of codelets to run in each step. Defaults to 20,000.
 