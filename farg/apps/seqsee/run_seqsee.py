# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

import argparse

from farg.apps.seqsee.batch_ui import SeqseeBatchUI
from farg.apps.seqsee.controller import SeqseeController
from farg.apps.seqsee.gui.gui import SeqseeGUI
from farg.apps.seqsee.read_input_spec import SeqseeReadInputSpec
from farg.apps.seqsee.stopping_conditions import SeqseeStoppingConditions
from farg.core.main import Main
import farg.flags as farg_flags
import sys

seqsee_parser = argparse.ArgumentParser(parents=[farg_flags.core_parser])
seqsee_parser.add_argument('--sequence', type=int, nargs='*')
seqsee_parser.add_argument('--unrevealed_terms', type=int, nargs='*')
seqsee_parser.add_argument('--double_mapping_resistance',
                           default=0.5, type=float,
                           help='Probability of not seeking a relation between two objects when a '
                                'relation exists')
seqsee_parser.add_argument("--use_group_distances", default=False, type=bool,
                           help="If true, distance between objects may be measured in groups. "
                                "For example, distance between 7 and 8 in '7 1 2 8' can be seen as "
                                "2 intervening elements or 1 intervening group.")


class UnprocessedFlags(object):
  pass

seqsee_parser.parse_args(args=None, namespace=UnprocessedFlags)

class SeqseeMain(Main):
  """
  The entry point into the Seqsee app. This controls all the modes of running Seqsee --- GUI,
  batch, and a side-by-side comparison with different flags.
  """
  #: The lowercase name of the program, used for such things as directory for ltm files
  #: and stats for batch runs.
  application_name = 'seqsee'
  #: The GUI class when running in GUI mode. The UI is responsible for interfacing between the
  #: user and the controller.
  gui_class = SeqseeGUI
  #: When running in batch mode, this class provides the UI. It also simulates the user: if
  #: the controller has a question that would have been fielded by the real user in GUI (such
  #: as "Are these the next terms?"), this UI tries to answer it based on future terms that
  #: have been provided to it.
  batch_ui_class = SeqseeBatchUI
  #: This class handles the central loop of the program. Its sole job is to mindlessly run
  #:  codelets which do the real work. In that sense, this is a "dumb" controller.
  controller_class = SeqseeController
  #: Lists stopping conditions that may be provided on the command-line in batch or SxS modes
  #: to get a sense of how long a program runs until this condition is met.
  #: Examples of conditions: A group spanning all terms is formed; a relation is formed
  #: with a certain type, and so forth.
  stopping_conditions_class = SeqseeStoppingConditions
  #: In batch/sxs modes, the various input sequences are read from a file. This class
  #: converts the file to input specifications.
  input_spec_reader_class = SeqseeReadInputSpec

  def ProcessCustomFlags(self):
    """
    Process Seqsee specific flags.
    """
    if not(self.flags.sequence) and (self.flags.run_mode == 'gui' or self.flags.run_mode == 'single'):
      print('No terms specified for the input sequence. Use --sequence ..., '
            'where the ... represents a space separated list of input integers.')
      sys.exit(1)

if __name__ == '__main__':
  SeqseeMain(UnprocessedFlags).Run()
