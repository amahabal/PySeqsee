#!/usr/bin/python

from apps.seqsee.flags import ParseSeqseeFlags
from apps.seqsee.controller import SeqseeController

flags = ParseSeqseeFlags()
print flags

controller = SeqseeController(flags)
# The following line takes control of the rest of the run(s):
ui = flags.ui(controller, flags)
ui.Launch()
