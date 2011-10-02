#!/usr/bin/python

from arguments import ParseSeqseeArguments
from run_state import RunState

args = ParseSeqseeArguments()
print args

run_state = RunState(args)
