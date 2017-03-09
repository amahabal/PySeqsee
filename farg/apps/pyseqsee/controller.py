import sys
from farg.apps.pyseqsee.codelets import CF_FocusOnObject, CF_FocusOnRandomElement
from farg.apps.pyseqsee.stream import PSStream
from farg.apps.pyseqsee.utils import PSObjectFromStructure
from farg.apps.pyseqsee.workspace import PSWorkspace
from farg.core.controller import Controller
from farg.core.ltm.manager import LTMManager
import farg.flags as farg_flags

kLTMName = "pyseqsee.main"


def _InitializePySeqseeLTM(ltm):
  for magnitude in range(10):
    ltm.GetNode(content=PSObjectFromStructure(magnitude))


LTMManager.RegisterInitializer(kLTMName, _InitializePySeqseeLTM)


class PSController(Controller):
  stream_class = PSStream
  workspace_class = PSWorkspace
  ltm_name = kLTMName
  routine_codelets_to_add = ((CF_FocusOnRandomElement, 30, 0.2),)

  def __init__(self, get_input_from_flags=True, **args):
    Controller.__init__(self, **args)
    if get_input_from_flags:
      self.SetInput(farg_flags.FargFlags.sequence,
                    farg_flags.FargFlags.unrevealed_terms)
    # Add the codelet to focus on the first object.
    if self.workspace.KnownElementCount() > 0:
      self.AddCodelet(
          family=CF_FocusOnObject,
          urgency=100,
          arguments_dict=dict(focus=self.workspace.GetFirstElement()))

  def SetInput(self, sequence, unrevealed_terms):
    self.workspace.InsertElements(sequence, log_msg="Initial input")
    self.unrevealed_terms = unrevealed_terms
