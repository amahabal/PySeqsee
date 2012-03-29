"""The Main class is the entry point into an app.
"""
from tide.run_mode import RunModeGUI, RunModeBatch, RunModeSxS
from third_party import gflags
import logging
import sys

FLAGS = gflags.FLAGS

gflags.DEFINE_enum('run_mode', 'gui',
                   ('gui', 'batch', 'sxs'),
                   'Mode to run in.')
gflags.DEFINE_enum('debug', '', ('', 'debug', 'info', 'warn', 'error', 'fatal'),
                   'Show messages from what debug level and above?')

class Main:
  run_mode_gui_class = RunModeGUI
  run_mode_batch_class = RunModeBatch
  run_mode_sxs_class = RunModeSxS

  def ProcessFlags(self):
    """Called after flags have been read in."""
    run_mode_name = FLAGS.run_mode
    if run_mode_name == 'gui':
      self.run_mode = self.run_mode_gui_class()
    elif run_mode_name == 'batch':
      self.run_mode = self.run_mode_batch_class()
    else:
      self.run_mode = self.run_mode_sxs_class()

    if FLAGS.debug:
      numeric_level = getattr(logging, FLAGS.debug.upper(), None)
      if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % FLAGS.debug)
      logging.basicConfig(level=numeric_level)

    self.ProcessCustomFlags()

  def ProcessCustomFlags(self):
    pass

  def Run(self):
    self.run_mode.Run()

  def main(self, argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError as e:
      print('%s\nUsage: %s ARGS\n%s\n\n%s' % (e, sys.argv[0], FLAGS, e))
      sys.exit(1)

    self.ProcessFlags()
    self.Run()
