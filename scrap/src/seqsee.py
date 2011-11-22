#!/usr/bin/python

from arguments import ParseSeqseeArguments
from runstate import RunState

args = ParseSeqseeArguments()
print args

runstate = RunState(args)
# The following line takes control of the rest of the run(s):
args.ui(runstate)
