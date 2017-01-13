import argparse

from farg.apps.bongard.batch_ui import BongardBatchUI
from farg.apps.bongard.controller import BongardController
from farg.apps.bongard.gui.gui import BongardGUI
from farg.apps.bongard.read_input_spec import BongardReadInputSpec
from farg.apps.bongard.stopping_conditions import BongardStoppingConditions
from farg.core.main import Main
import sys
import farg_flags

bongard_parser = argparse.ArgumentParser(parents=[farg_flags.core_parser])
# Flags for specifying the input and, for use in testing, expected output.
bongard_parser.add_argument('--left', type=int, nargs='*')
bongard_parser.add_argument('--right', type=int, nargs='*')
bongard_parser.add_argument('--expected_output')

class UnprocessedFlags(object):
  pass

bongard_parser.parse_args(args=None, namespace=UnprocessedFlags)

class BongardMain(Main):
  """
  The entry point into the Bongard app. This controls all the modes of running
  Bongard --- GUI, batch, and a side-by-side comparison with different flags.
  """
  #: The lowercase name of the program, used for such things as directory for ltm files
  #: and stats for batch runs.
  application_name = 'bongard'

  #: The GUI class when running in GUI mode. The UI is responsible for interfacing between the
  #: user and the controller.
  gui_class = BongardGUI

  #: When running in batch mode, this class provides the UI. It also simulates the user: if
  #: the controller has a question that would have been fielded by the real user in GUI (such
  #: as "Are these the next terms?"), this UI tries to answer it based on future terms that
  #: have been provided to it.
  batch_ui_class = BongardBatchUI

  #: This class handles the central loop of the program. Its sole job is to mindlessly run
  #: codelets which do the real work. In that sense, this is a "dumb" controller.
  controller_class = BongardController

  #: Lists stopping conditions that may be provided on the command-line in batch or SxS modes
  #: to get a sense of how long a program runs until this condition is met.
  #: Examples of conditions: A group spanning all terms is formed; a relation is formed
  #: with a certain type, and so forth.
  stopping_conditions_class = BongardStoppingConditions

  #: In batch/sxs modes, the various input sequences are read from a file. This class
  #: converts the file to input specifications.
  input_spec_reader_class = BongardReadInputSpec

  def ProcessCustomFlags(self):
    """
    Process Bongard specific flags.
    """
    overlap = set(self.flags.left).intersection(self.flags.right) 
    if overlap:
      sys.exit("It makes no sense for the --left and --right to share elements as they do here: " +
               str(overlap))

if __name__ == '__main__':
  BongardMain(UnprocessedFlags).Run()

