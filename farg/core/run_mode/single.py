# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

from farg.core.exceptions import BatchModeStopException
from farg.core.run_mode.non_interactive import RunModeNonInteractive
from farg.third_party import gflags
from io import StringIO
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
