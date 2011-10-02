import argparse
import sys

# Corresponding Perl code in Seqsee.pm

def ParseSeqseeArguments():
  parser = argparse.ArgumentParser(
      description="Seqsee: A cognitive architecture for integer sequence "
                  "perception")
  parser.add_argument('sequence', metavar='N', type=int, nargs='+',
                      help='terms of the sequence')
  parser.add_argument('--coderack_size', default=10, type=int)
  parser.add_argument('--ui',
                      help='Type of ui (cmdline, gui, batch)',
                      choices=['cmdline', 'gui', 'batch'],
                      default='gui')
  parser.add_argument('--unrevealed_terms',
                      help='Extra terms (which Seqsee will ignore expcept in batch mode)',
                      default='')

  # Parse
  args = parser.parse_args()
  
  # Validate
  supported_uis = ['gui']
  if args.ui not in supported_uis:
    print "%s is not a supported UI (yet)" % args.ui
    sys.exit(1)

  # Pre-process
  args.unrevealed_terms = args.unrevealed_terms.split()

  return args