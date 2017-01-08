Running a single example
===========================

This section uses the Seqsee app to illustrate how to run an app.

Flags supported by Seqsee
---------------------------

For the current purpose of showing how to run it, I will mention the single flag --sequence, which
specifies the input terms.

One may thus write::

    --sequence 1 2 3 4 5
    
to specify these numbers as the input to the sequence.

Command
---------

This command, run in the Pyseqsee directory, will start a graphical window (using Tkinter)::

  python3 -m farg.apps.seqsee.run_seqsee --sequence 1 2 3 4 5

Start the processing
----------------------

You need to press the key "c" (for continue) to set the application in motion. You could also use
repeated "s" to step through the processing.

Different Views
-----------------

By default, what is shown is the Workspace. This is the set of objects and relations. But the menu
at the top may be used to change the view to also include the Coderack (which is a set of actions
waiting in the wings, one of which will be chosen next to run), the Stream of Thought (which is a
series of recently focused-on items that the application is likely to be reminded of as it proceeds),
and the Slipnet (which shows the activation levels of various concepts, things that the program has
judged to be relevant to the task at hand). 


Flags supported by all apps
------------------------------

--run_mode
^^^^^^^^^^^^

This can take the values "gui" (which is the default, and starts a graphical interface), "batch" (which
can run many inputs multiple times and store the stats), "sxs" (which can compare different sets of
flags), and "single" (which runs a single example once, and is primarily intended for use by the
batch and xsx modes).

--use_stored_ltm
^^^^^^^^^^^^^^^^^^

Applications can learn and improve over time. By default, in the "gui" mode, the previously stored
long-term memory is used. In batch mode, of course, this is turned off by default to keep runs
independent of each other.

--gui_canvas_height, --gui_canvas_width
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These can be used to change the size of the GUI window.

All core flags
--------------------------------

The module farg_flags.py in the top directory defines the shared flags.

