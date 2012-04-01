"""The Main class is the entry point into an app.
"""
from tide.run_mode import batch, gui, sxs
from third_party import gflags
import logging
import sys
from tide.ui.gui import GUI
from tide.ui.batch_ui import BatchUI

FLAGS = gflags.FLAGS

gflags.DEFINE_enum('run_mode', 'gui',
                   ('gui', 'batch', 'sxs'),
                   'Mode to run in.')
gflags.DEFINE_enum('debug', '', ('', 'debug', 'info', 'warn', 'error', 'fatal'),
                   'Show messages from what debug level and above?')

class Main:
  run_mode_gui_class = gui.RunModeGUI
  run_mode_batch_class = batch.RunModeBatch
  run_mode_sxs_class = sxs.RunModeSxS

  gui_class = GUI
  batch_ui_class = BatchUI

  from tide.controller import Controller
  controller_class = Controller

  def ProcessFlags(self):
    """Called after flags have been read in."""
    self.ProcessCustomFlags()

    run_mode_name = FLAGS.run_mode
    if run_mode_name == 'gui':
      self.run_mode = self.run_mode_gui_class(controller_class=self.controller_class,
                                              ui_class=self.gui_class)
    elif run_mode_name == 'batch':
      self.run_mode = self.run_mode_batch_class(controller_class=self.controller_class,
                                                ui_class=self.batch_ui_class)
    else:
      self.run_mode = self.run_mode_sxs_class(controller_class=self.controller_class,
                                              ui_class=self.batch_ui_class)

    if FLAGS.debug:
      numeric_level = getattr(logging, FLAGS.debug.upper(), None)
      if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % FLAGS.debug)
      logging.basicConfig(level=numeric_level)

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
