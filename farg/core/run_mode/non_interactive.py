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

from farg.core.run_mode.run_mode import RunMode
import subprocess
import sys

class RunModeNonInteractive(RunMode):
  def DoSingleRun(self, cmdline_arguments_dict, extra_arguments=None):
    arguments = []  # Collect arguments to pass to subprocess
    arguments.append(sys.executable)  # Python executable
    arguments.append(sys.argv[0])  # The script used to run this mode (e.g., run_seqsee.py)

    arguments.extend('--%s=%s' % (str(k), str(v)) for k, v in cmdline_arguments_dict.items())
    if extra_arguments:
      arguments.append(extra_arguments)
    return subprocess.check_output(arguments)
