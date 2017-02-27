from farg.apps.pyseqsee.stream import PSStream
from farg.apps.pyseqsee.workspace import PSWorkspace
from farg.core.controller import Controller
import farg.flags as farg_flags


class PSController(Controller):
  stream_class = PSStream
  workspace_class = PSWorkspace

  def __init__(self, get_input_from_flags=True, **args):
    Controller.__init__(self, **args)
    if get_input_from_flags:
      self.SetInput(farg_flags.FargFlags.sequence,
                    farg_flags.FargFlags.unrevealed_terms)

  def SetInput(self, sequence, unrevealed_terms):
    self.workspace.InsertElements(sequence)
    self.unrevealed_terms = unrevealed_terms
