import sys

from farg.apps.bongard.categories import Square
from farg.apps.bongard.workspace import BongardWorkspace, PlatonicInteger
from farg.core.controller import Controller
from farg.core.ltm.edge import LTMEdge
from farg.core.ltm.manager import LTMManager
import farg.flags as farg_flags
kLTMName = 'bongard.main'

def InitializeBongardLTM(ltm):
  """Called if ltm was empty (had no nodes)."""
  for i in range(10):
    ltm.GetNode(content=PlatonicInteger(magnitude=i))
  for i in (0, 4, 9):
    ltm.AddEdge(PlatonicInteger(magnitude=i), Square(),
                edge_type_set={LTMEdge.LTM_EDGE_TYPE_ISA})

LTMManager.RegisterInitializer(kLTMName, InitializeBongardLTM)

class BongardController(Controller):
  """Controller for Bongard."""
  # EDIT-ME: possibly set up routine_codelets_to_add.
  workspace_class = BongardWorkspace
  ltm_name = kLTMName

  def __init__(self, **args):
    Controller.__init__(self, **args)
    self.workspace.SetItems(farg_flags.FargFlags.left, farg_flags.FargFlags.right)

    from farg.apps.bongard.codelet_families.all import CF_HorribleHack
    self.AddCodelet(family=CF_HorribleHack, urgency=100)