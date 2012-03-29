Run Mode
==========

It is possible to run Tide applications in several modes. These include:

* GUI. In this mode, the program is run interactively.
* Batch. In this mode, the program is run several times on a set of inputs and
  a performance report is generated.
* SxS (which stands for "side-by-side"). Two versions of the program (differentiated
  by some flag, for instance) are run several times on a set of inputs in order
  to compare the performance of the two versions.

API
------

Each run mode is a subclass of tide.RunMode. There is a single public method in
this class::
 
  run_mode.Run()  # Flags control what happens.

GUI
-----

This run mode is specified by the command-line flag::

  --run_mode=GUI

It starts up the ui in the class UI.Interactive. This ui owns a controller that
the user can step through, pause, and so forth.

Batch
------

This run mode is specified by the command-line flag::

  --run_mode=Batch

Another flag controls the file from which input is read and the report location::

  --input_specification_file=/some/file
  --report_path=/some/other

.. note::

  What class/function parses the input file? This needs to be figured out. One
  possibility is that one must subclass the RunMode and specify an InputParser.

SxS
------

This run mode is specified by the command-line flag::

  --run_mode=SxS

Another flag controls the file from which input is read and the report location::

  --input_specification_file=/some/file
  --report_path=/some/other

Number of times each sequence is run::

  --sxs_repetitions=20  # How many times to repeat for each input.


.. note::

  The same caveat as before applies.

Other flags control the two versions used::

  --sxs_base_flags='...flags for base...'
  --sxs_exp_flags='...flags for exp...'
  --sxs_repetitions=20  # How many times to repeat for each input.

