import argparse
import sys

from farg.apps.pyseqsee.stream import PSController
from farg.apps.pyseqsee.ui import PySeqseeGUI, PySeqseeBatchUI
from farg.apps.seqsee.read_input_spec import SeqseeReadInputSpec
from farg.core.main import Main
from farg.core.stopping_conditions import StoppingConditions
import farg.flags as farg_flags
pyseqsee_parser = argparse.ArgumentParser(parents=[farg_flags.core_parser])
pyseqsee_parser.add_argument('--sequence', type=int, nargs='*')
pyseqsee_parser.add_argument('--unrevealed_terms', type=int, nargs='*')


class UnprocessedFlags(object):
  pass
pyseqsee_parser.parse_args(args=None, namespace=UnprocessedFlags)

class PSStoppingConditions(StoppingConditions):
  pass

class PySeqseeMain(Main):
  application_name = 'pyseqsee'
  gui_class = PySeqseeGUI
  batch_ui_class = PySeqseeBatchUI
  controller_class = PSController
  stopping_conditions_class = PSStoppingConditions
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
  PySeqseeMain(UnprocessedFlags).Run()
