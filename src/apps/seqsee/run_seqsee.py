#!/usr/bin/python

from apps.seqsee.controller import SeqseeController
from apps.seqsee.gui.gui import SeqseeGUI
from third_party import gflags
import logging
import sys

FLAGS = gflags.FLAGS

gflags.DEFINE_enum('ui', 'gui', ('gui', 'cmdline', 'batch', 'web'),
                   'Which UI to use?')

gflags.DEFINE_enum('debug', '', ('', 'debug', 'info', 'warn', 'error', 'fatal'),
                   'Show messages from what debug level and above?')

gflags.DEFINE_spaceseplist('sequence', '',
                           'A space separated list of integers')

gflags.DEFINE_spaceseplist('unrevealed_terms', '',
                           'A space separated list of integers')


def ProcessFlags():
  if FLAGS.ui == 'gui':
    FLAGS.ui = SeqseeGUI
  elif FLAGS.ui == 'cmdline':
    from farg.ui.cmdline import CmdlineUI
    FLAGS.ui = CmdlineUI
  else:
    # TODO(#20 --- Dec 28, 2011): Add support for cmdline mode.
    # TODO(#21 --- Dec 28, 2011): Add support for web mode.
    print "UI '%s' is not supported (yet)" % FLAGS.ui
    sys.exit(1)

  FLAGS.sequence = [int(x) for x in FLAGS.sequence]
  FLAGS.unrevealed_terms = [int(x) for x in FLAGS.unrevealed_terms]

  if FLAGS.debug:
    numeric_level = getattr(logging, FLAGS.debug.upper(), None)
    if not isinstance(numeric_level, int):
      raise ValueError('Invalid log level: %s' % FLAGS.debug)
    logging.basicConfig(level=numeric_level)

def main(argv):
  try:
    argv = FLAGS(argv)  # parse flags
  except gflags.FlagsError, e:
    print '%s\nUsage: %s ARGS\n%s\n\n%s' % (e, sys.argv[0], FLAGS, e)
    sys.exit(1)

  ProcessFlags()

  controller = SeqseeController()
  # The following line takes control of the rest of the run(s):
  ui = FLAGS.ui(controller)
  ui.Launch()

if __name__ == '__main__':
  main(sys.argv)
