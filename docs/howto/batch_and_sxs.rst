Evaluation: Batch mode and side-by-side mode
==============================================

I will again assume a hypothetical app named 'cat'.

The batch mode is useful for running the program multiple times on various inputs
and collecting the statistics. To use this mode, you need to add::

  --run_mode=batch

The Side-by-side mode allows comparison of two settings of the program by running
the program multiple times on various inputs. It is specified using::

  --run_mode=sxs

Screenshot
------------

Here is a screenshot of a batch mode run of Seqsee where the previous run had
been hobbled, resulting in the current run being better. The left column shown
input sequences, color coded to show what sequences improved (green) or got worse
(red). White indicates no significant change (at 95% confidence).

.. image:: ../images/batch_diff.png
  :height: 300px
  :align: center

Flags shared by both SxS and Batch
-----------------------------------

--num_iterations=N
********************

How many times to run for each input.

--max_steps=N
****************

Maximum number of steps to run for each.

--input_spec_file=filename
***************************

File containing inputs on which to run. The format of this file is described
below.

Reading the input
*******************

The class that reads the input is a subclass of ReadInputSpec in 'farg/core/read_input_spec.py'.
If your input is line based, you can get by with just overriding 'ReadLine'. Non-comment
non-empty lines are sent to this function, and it should return a SpecificationForOneRun object.
This merely has a name for the input and command line flags to be used during the run.

For Seqsee, the line reader splits on '|' and returns a SpecificationForOneRun::

  def ReadLine(self, line):
    if not '|' in line:
      return
    input, continuation = (x.split() for x in line.strip().split('|'))
    yield SpecificationForOneRun(' '.join(input),  # name
                                 dict(sequence=' '.join(input),
                                      unrevealed_terms=' '.join(continuation)))

If your input does not fit well on a single line, you can override the ReadFile
method and you can parse it in whatever way and return a bunch of SpecificationForOneRun.

Running in Batch mode
------------------------

Running a side-by-side comparison
------------------------------------


How to specify a stopping condition
-------------------------------------
