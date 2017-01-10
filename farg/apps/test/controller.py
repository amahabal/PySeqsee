from farg.apps.test.workspace import TestWorkspace
from farg.core.controller import Controller
from farg.core.ltm.manager import LTMManager
import sys

# If you need access to flags, you need:
# import farg_flags
# # The flag --foo is available at farg_flags.FargFlags.foo

kLTMName = 'test.main'

def InitializeTestLTM(ltm):
  """Called if ltm was empty (had no nodes)."""
  pass

LTMManager.RegisterInitializer(kLTMName, InitializeTestLTM)

class TestController(Controller):
  """Controller for Test."""
  # EDIT-ME: possibly set up routine_codelets_to_add.
  workspace_class = TestWorkspace
  ltm_name = kLTMName

  def __init__(self, *, ui, controller_depth=0,
               parent_controller=None, workspace_arguments=None,
               stopping_condition=None):
    Controller.__init__(self, ui=ui, parent_controller=parent_controller,
                        workspace_arguments=workspace_arguments,
                        stopping_condition=stopping_condition)

