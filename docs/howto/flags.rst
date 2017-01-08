How to add flags to the application
====================================

Flags are processed using argparse, and a limited amount of "distributed" flag definition is
supported --- several flags are defined in the core (in farg_flags.py), and each application extends
this by adding its own flags.

Where the flags are defined
-----------------------------

Core flags are defined in 'farg_flags.py', which defines the flags parser called 'core_parser'. The
entry point for each app extends this. Currently, in Seqsee (run_seqsee.py), we see::

  import farg_flags
  seqsee_parser = argparse.ArgumentParser(parents=[farg_flags.core_parser])
  seqsee_parser.add_argument('--sequence', type=int, nargs='*')

Processing of flags
------------------------

Flag values are processed to obtain complex default values (for example, the default value of the
flag '--stats_directory' depends on the value of the flag '--persistent_directory', as the stats
directory is a subdirectory in that directory.

Sanity checking is also done along with creation of directories as needed.

All this happens in the constructor of the farg.core.main.Main, which get passed in the unprocessed
flags. The entry point of each app is a subclass of Main.

While processing flags, a call is made to ProcessCustomFlags, which the Main class of the app can
define if it wishes to process the flags that it has defined (as Seqsee could have done for the flag
--sequence).

The processed flags are available as self.flags in the Main class.

The entry point of apps
--------------------------

To summerize, here are the relevant bits of the Seqsee app's entry point::

  import argparse
  import farg_flags
  from farg.core.main import Main
  
  seqsee_parser = argparse.ArgumentParser(parents=[farg_flags.core_parser])
  seqsee_parser.add_argument('--sequence', type=int, nargs='*')
  
  class UnprocessedFlags(object):
    pass

  seqsee_parser.parse_args(args=None, namespace=UnprocessedFlags)
  class SeqseeMain(Main):
     def ProcessCustomFlags(self):
       # can access self.flags with the core flags already processed
       pass

  if __name__ == '__main__':
    SeqseeMain(UnprocessedFlags).Run()


Where the flags get stored
----------------------------------

Flags, after processing, end up both in Main.flags and farg_flags.FargFlags. Other modules will use
this latter route for accessing. A module may say::

  import farg_flags
  if farg_flags.FargFlags.use_stored_ltm:
    Do something

