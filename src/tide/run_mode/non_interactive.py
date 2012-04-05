from tide.run_mode.run_mode import RunMode
import sys
import subprocess
class RunModeNonInteractive(RunMode):
  def DoSingleRun(self, cmdline_arguments_dict):
    arguments = []  # Collect arguments to pass to subprocess
    arguments.append(sys.executable)  # Python executable
    arguments.append(sys.argv[0])  # The script used to run this mode (e.g., run_seqsee.py)

    arguments.extend('--%s=%s' % (str(k), str(v)) for k, v in cmdline_arguments_dict.items())
    return subprocess.check_output(arguments)
