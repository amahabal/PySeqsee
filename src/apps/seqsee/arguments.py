"""Argument processing for Seqsee."""
import argparse
import logging
import sys

from apps.seqsee.gui.gui import SeqseeGUI

# Corresponding Perl code in Seqsee.pm

def ParseSeqseeArguments():
  parser = argparse.ArgumentParser(
      description="Seqsee: A cognitive architecture for integer sequence perception",
      prog='PySeqsee',)
  parser.add_argument('--version', action='version', version='%(prog)s 0.01')
  parser.add_argument('sequence', metavar='N', type=int, nargs='+',
                      help='terms of the sequence')
  parser.add_argument('--ui',
                      help='Type of ui (cmdline, gui, batch, web). Only gui implemented',
                      choices=['cmdline', 'gui', 'batch', 'web'],
                      default='gui')
  parser.add_argument('--unrevealed_terms',
                      help='Extra terms (which Seqsee will ignore expcept in batch mode)',
                      default='')
  parser.add_argument('--debug', default='', help='Logging level')

  parser.add_argument('--gui_initial_view', default='ws',
                      help='In GUI mode, this is the initial view to show.')
  parser.add_argument('--gui_canvas_height', default=400, type=int,
                      help='In GUI mode, height of the ws canvas.')
  parser.add_argument('--gui_canvas_width', default=800, type=int,
                      help='In GUI mode, width of the ws canvas.')
  parser.add_argument('--gui_show_ltm', action='store_true',
                      help='Whether to show the LTM.')

  # Parse
  args = parser.parse_args()

  # Validate and Pre-process
  if args.ui is 'gui':
    args.ui = SeqseeGUI
  else:
    # TODO(#20 --- Dec 28, 2011): Add support for cmdline mode.
    # TODO(#21 --- Dec 28, 2011): Add support for web mode.
    print "%s is not a supported UI (yet)" % args.ui
    sys.exit(1)

  args.unrevealed_terms = [int(x) for x in args.unrevealed_terms.split()]

  if args.debug:
    numeric_level = getattr(logging, args.debug.upper(), None)
    if not isinstance(numeric_level, int):
      raise ValueError('Invalid log level: %s' % args.debug)
    logging.basicConfig(level=numeric_level)

  return args
