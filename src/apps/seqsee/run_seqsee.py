#!/usr/bin/python

from apps.seqsee.arguments import ParseSeqseeArguments
from apps.seqsee.controller import SeqseeController

args = ParseSeqseeArguments()
print args

controller = SeqseeController()
# The following line takes control of the rest of the run(s):
ui = args.ui(controller)
ui.Launch()
