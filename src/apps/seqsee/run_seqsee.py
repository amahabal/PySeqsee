#!/usr/bin/python

from apps.seqsee.arguments import ParseSeqseeArguments
from apps.seqsee.runstate import SeqseeRunState
from farg.controller import Controller

args = ParseSeqseeArguments()
print args

runstate = SeqseeRunState(args)
controller = Controller(runstate)
# The following line takes control of the rest of the run(s):
ui = args.ui(controller)
ui.Launch()
