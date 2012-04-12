from farg.exceptions import BatchModeStopException
from farg.run_mode.non_interactive import RunModeNonInteractive
from io import StringIO
from third_party import gflags
import sys

FLAGS = gflags.FLAGS

class RunModeSingle(RunModeNonInteractive):
  """
  Run mode for a single run as part of a batch run or a SxS run.
  
  This class is responsible for running the program once, suppressing its output, and
  producing an easy to parse string.
  """
  def __init__(self, *, controller_class, ui_class, stopping_condition_fn):
    self.ui = ui_class(controller_class=controller_class,
                       stopping_condition_fn=stopping_condition_fn)

  def Run(self):
    saved_stdout = sys.stdout
    sys.stdout = StringIO()
    output_status = ''
    try:
      self.ui.Run()
    except BatchModeStopException as e:
      classname = str(e.__class__).split('.')[-1][:-2]
      output_status = '%s %d' % (classname, e.codelet_count)
    else:
      output_status = 'MaxCodeletsReached'
    finally:
      sys.stdout = saved_stdout
      print(output_status)
