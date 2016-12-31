Creating a New FARG Application
================================

This tutorial will describe the process of creating a full new application. It will
attempt to touch all aspects of the process.

The application developed in this tutorial may be called "Numeric Bongard". Unlike
Bongard problems, this will not be images.

I imagine a command-line such as::

  run_numeric_bongard.py --left="3 7 11" --right="2 8 4 16"

And it should print something out about evens and odds.

This is a rich domain::

  --left="3 7 11" --right="9 15 21"  ==> prime/composite
  --left="3 7 11" --right="5 13 17"  ==> 3 mod 4 vs 1 mod 4
  --left="3 7 11" --right="2 5 13 17"  ==> 3 mod 4 vs not(3 mod 4)
  --left="3 7 11" --right="2 5 13 17 15"  ==> 3 mod 4 primes vs not(3 mod 4 primes)

.. toctree::
   :maxdepth: 2

   running_create_app
   adding_input_flags
   setting_up_workspace
   adding_categories
