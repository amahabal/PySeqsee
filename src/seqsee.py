#!/usr/bin/python

from arguments import ParseSeqseeArguments
from run_state import RunState

args = ParseSeqseeArguments()
print args

run_state = RunState(args)
# The following line takes control of the rest of the run(s):
args.ui(run_state)