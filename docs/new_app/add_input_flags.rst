Adding flags to specify inputs
================================

We need a way to tell the app what the two sets of items are. One possible invocation we can have is::

  farg run bongard --left 1 3 5 7 -- right 2 4 6 8

This is what we will now enable.

Updating farg/apps/bongard/run_bongard.py
----------------------------------------------

The file run_bongard.py has two flags already present: '--input' and '--expected_output'. We will
replace the first of these with the two flags we want::

  bongard_parser.add_argument('--left', type=int, nargs='*')
  bongard_parser.add_argument('--right', type=int, nargs='*')

The 'add_argument' method is from the :py:mod:`argparse` module. 'type=int' tells the argument parser to expect
integers, and the 'nargs=*' tells it that there are arbitrarily many of these.

Sanity checking the flags
---------------------------

For this app, it makes no sense for the two sets to overlap: we are looking for an explanation that
applies to all the left elements and to none of the right elements. We will check for this in the
'ProcessCustomFlags' method in 'run_bongard.py', which is currently empty::

  class BongardMain(Main):
    def ProcessCustomFlags(self):
      if not self.flags.left:
        sys.exit("Required argument --left missing or empty")
      if not self.flags.right:
        sys.exit("Required argument --right missing or empty")
      overlap = set(self.flags.left).intersection(self.flags.right) 
      if overlap:
        sys.exit("It makes no sense for the --left and --right to share elements as they do here: " +
                 str(overlap))
      
In this function, we could have changed the flags in some way if we needed to, or even manufactured
"synthetic" flags as needed (by putting them in self.flags).

Accessing flags from other files
----------------------------------

These flags will be needed in other parts of the app. In any file needing them, add the following
lines::

  import farg.flags as farg_flags

  # later...
  farg_flags.FargFlags.left