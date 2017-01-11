import argparse

from farg.apps.test.batch_ui import TestBatchUI
from farg.apps.test.controller import TestController
from farg.apps.test.gui.gui import TestGUI
from farg.apps.test.read_input_spec import TestReadInputSpec
from farg.apps.test.stopping_conditions import TestStoppingConditions
from farg.core.main import Main
import sys
import farg_flags

test_parser = argparse.ArgumentParser(parents=[farg_flags.core_parser])
# Flags for specifying the input and, for use in testing, expected output.
test_parser.add_argument('--input')
test_parser.add_argument('--expected_output')

class UnprocessedFlags(object):
  pass

test_parser.parse_args(args=None, namespace=UnprocessedFlags)

class TestMain(Main):
  """
  The entry point into the Test app. This controls all the modes of running
  Test --- GUI, batch, and a side-by-side comparison with different flags.
  """
  #: The lowercase name of the program, used for such things as directory for ltm files
  #: and stats for batch runs.
  application_name = 'test'

  #: The GUI class when running in GUI mode. The UI is responsible for interfacing between the
  #: user and the controller.
  gui_class = TestGUI

  #: When running in batch mode, this class provides the UI. It also simulates the user: if
  #: the controller has a question that would have been fielded by the real user in GUI (such
  #: as "Are these the next terms?"), this UI tries to answer it based on future terms that
  #: have been provided to it.
  batch_ui_class = TestBatchUI

  #: This class handles the central loop of the program. Its sole job is to mindlessly run
  #: codelets which do the real work. In that sense, this is a "dumb" controller.
  controller_class = TestController

  #: Lists stopping conditions that may be provided on the command-line in batch or SxS modes
  #: to get a sense of how long a program runs until this condition is met.
  #: Examples of conditions: A group spanning all terms is formed; a relation is formed
  #: with a certain type, and so forth.
  stopping_conditions_class = TestStoppingConditions

  #: In batch/sxs modes, the various input sequences are read from a file. This class
  #: converts the file to input specifications.
  input_spec_reader_class = TestReadInputSpec

  def ProcessCustomFlags(self):
    """
    Process Test specific flags.
    """
    #: The processed version of core flags is available as self.flags.
    pass

if __name__ == '__main__':
  TestMain(UnprocessedFlags).Run()

