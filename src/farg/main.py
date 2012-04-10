"""The Main class is the entry point into an app.
"""
from farg.ui.batch_ui import BatchUI
from farg.ui.gui import GUI
from third_party import gflags
from tide.run_mode import batch, gui, single, sxs
import logging
import sys

FLAGS = gflags.FLAGS

gflags.DEFINE_enum('run_mode', 'gui',
                   ('gui', 'batch', 'sxs', 'single'),
                   'Mode to run in.')
gflags.DEFINE_enum('debug', '', ('', 'debug', 'info', 'warn', 'error', 'fatal'),
                   'Show messages from what debug level and above?')
gflags.DEFINE_string('stopping_condition', None, "Stopping condition, if any")

gflags.DEFINE_string('input_spec_file', None,
                     'Path specifying inputs over which to run bach processes.')
gflags.DEFINE_integer('num_iterations', 10,
                      "In batch and SxS mode, number of iterations to run", 1)
gflags.DEFINE_integer('max_steps', 1000,
                      "In batch and SxS mode, number of steps per run", 1)

class Main:
  run_mode_gui_class = gui.RunModeGUI
  run_mode_batch_class = batch.RunModeBatch
  run_mode_sxs_class = sxs.RunModeSxS
  run_mode_single_run_class = single.RunModeSingle

  gui_class = GUI
  batch_ui_class = BatchUI

  from farg.controller import Controller
  controller_class = Controller

  stopping_conditions = dict()

  input_spec_reader_class = None

  def VerifyStoppingConditionSanity(self):
    run_mode_name = FLAGS.run_mode
    stopping_condition = FLAGS.stopping_condition
    if run_mode_name == 'gui':
      # There should be no stopping condition.
      if stopping_condition:
        raise ValueError("Stopping condition does not make sense with GUI.")
    else:  # Verify that the stopping condition's name is defined.
      if FLAGS.stopping_condition and FLAGS.stopping_condition != "None":
        if FLAGS.stopping_condition not in self.stopping_conditions:
          raise ValueError('Unknown stopping condition %s. Use one of %s' %
                           (FLAGS.stopping_condition, list(self.stopping_conditions.keys())))
        else:
          self.stopping_condition_fn = self.stopping_conditions[FLAGS.stopping_condition]
      else:
        self.stopping_condition_fn = ''

  def CreateRunModeInstance(self):
    run_mode_name = FLAGS.run_mode
    if run_mode_name == 'gui':
      return self.run_mode_gui_class(controller_class=self.controller_class,
                                     ui_class=self.gui_class)
    elif run_mode_name == 'single':
      return self.run_mode_single_run_class(controller_class=self.controller_class,
                                            ui_class=self.batch_ui_class,
                                            stopping_condition_fn=self.stopping_condition_fn)
    else:
      if not FLAGS.input_spec_file:
        error_msg = ('Runmode --run_mode=%s requires --input_spec_file to be specified' %
                     run_mode_name)
        raise ValueError(error_msg)
      input_spec = list(self.input_spec_reader_class().ReadFile(FLAGS.input_spec_file))
      print(input_spec)
      if run_mode_name == 'batch':
        return self.run_mode_batch_class(controller_class=self.controller_class,
                                         input_spec=input_spec)
      elif run_mode_name == 'sxs':
        return self.run_mode_sxs_class(controller_class=self.controller_class,
                                       input_spec=input_spec)
      else:
        raise ValueError("Unrecognized run_mode %s" % run_mode_name)

  def ProcessFlags(self):
    """Called after flags have been read in."""
    self.ProcessCustomFlags()

    self.VerifyStoppingConditionSanity()
    self.run_mode = self.CreateRunModeInstance()

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
