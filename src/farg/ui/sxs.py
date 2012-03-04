from farg.ui.ui import UI

import time

from third_party import gflags
import subprocess
FLAGS = gflags.FLAGS

gflags.DEFINE_string('sxs_flag', '', 'Flag on which to base the side-by-side comparison')

gflags.DEFINE_string('sxs_condition', '',
                     'A string indicating a condition')

gflags.DEFINE_integer('sxs_max_steps', 5000,
                      'Maximum number of steps for a single run')

gflags.DEFINE_integer('sxs_number_of_runs', 5,
                      'Number of runs for each side')

class SxSUIHelper(UI):
  """A UI for running a single run when doing a SxS."""

  def __init__(self, controller):
    if not FLAGS.sxs_condition:
      raise gflags.FlagsError('Must specify --sxs_condition when --ui=sxs.')
    UI.__init__(self, controller)


  def Launch(self):
    """Starts the app by launching the UI."""
    start_time = time.time()
    for _step in xrange(0, FLAGS.sxs_max_steps):
      self.controller.Step()
      if self.controller.CheckCondition():
        time_elasped = time.time() - start_time
        print "CONDITION MATCHED! Codelets run: %d (in %.3f seconds)" % (
            self.controller.steps_taken, time_elasped)
        import sys
        sys.exit()

  def DisplayMessage(self, message):
    print '[%d] Message: %s' % (self.controller.steps_taken, message)

  def AskYesNoQuestion(self, question):
    print '[%d] Question: %s' % (self.controller.steps_taken, question)
    ans = raw_input('[y/n] ').lower().find('y') >= 0
    print "You chose %s" % ans
    return ans


class SxSUI(UI):
  """A UI for running a side-by-side comparison of number of codelets and time taken
     for reaching some predefined state in two conditions, with and without a given flag.
  """

  def __init__(self, controller):
    if not FLAGS.sxs_flag:
      raise gflags.FlagsError('Must specify --sxs_flag when --ui=sxs.')
    UI.__init__(self, controller)

  def Launch(self):
    """Starts the app by launching the UI."""
    sequence_string = ' '.join(str(x) for x in FLAGS.sequence)
    arguments = ['src/apps/seqsee/run_seqsee.py',
                 '--ui', 'sxs_helper',
                 '--sxs_max_steps', str(FLAGS.sxs_max_steps),
                 '--sxs_condition', FLAGS.sxs_condition,
                 '--sequence', sequence_string]
    print arguments
    for idx in range(0, FLAGS.sxs_number_of_runs):
      print "Run #%d" % idx
      print subprocess.call(arguments)
