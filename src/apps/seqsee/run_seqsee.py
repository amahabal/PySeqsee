#!/usr/bin/python

from apps.seqsee.controller import SeqseeController
from third_party import gflags
import sys
import logging

#flags = ParseSeqseeFlags()
#print flags

FLAGS = gflags.FLAGS

gflags.DEFINE_enum('ui', 'gui', ('gui', 'cmdline', 'batch', 'web'),
                   'Which UI to use?')

gflags.DEFINE_string('gui_initial_view', 'ws',
                     'In GUI mode, what should the initial mode be?')

gflags.DEFINE_integer('gui_canvas_height', 400,
                      'Height of the central canvas')
gflags.DEFINE_integer('gui_canvas_width', 800,
                      'Width of the central canvas')
gflags.DEFINE_boolean('gui_show_ltm', False,
                      "Whether to show the LTM (it's expensive!)")

gflags.DEFINE_enum('debug', '', ('', 'debug', 'info', 'warn', 'error', 'fatal'),
                   'Show messages from what debug level and above?')

gflags.DEFINE_spaceseplist('sequence', '',
                           'A space separated list of integers')

gflags.DEFINE_spaceseplist('unrevealed_terms', '',
                           'A space separated list of integers')


def main(argv):
  try:
    argv = FLAGS(argv)  # parse flags
  except gflags.FlagsError, e:
    print '%s\nUsage: %s ARGS\n%s\n\n%s' % (e, sys.argv[0], FLAGS, e)
    sys.exit(1)

  if FLAGS.ui == 'gui':
    from apps.seqsee.gui.gui import SeqseeGUI
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


  controller = SeqseeController(FLAGS)
  # The following line takes control of the rest of the run(s):
  ui = FLAGS.ui(controller, FLAGS)
  ui.Launch()

if __name__ == '__main__':
  main(sys.argv)
