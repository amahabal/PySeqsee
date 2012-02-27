from farg.controller import Controller
from farg.meta import SubspaceMeta

class Subspace(object):
  __metaclass__ = SubspaceMeta

  WS = None

  @staticmethod
  def QuickReconn(**args):
    raise Exception("Attempt to call Subspace(). Surely you meant to call a subclass?")

  def InitializeCoderack(self):
    raise Exception("Base InitializeCoderack called. This should have been overridden "
                    "(to set up the initial codelet, for example)")

  def RoutineCodeletsToAdd(self):
    return None

  def __init__(self, parent_controller, nsteps, workspace_arguments):
    self.controller = Controller(routine_codelets_to_add=self.RoutineCodeletsToAdd())
    self.controller.ui = parent_controller.ui
    self.workspace = self.controller.workspace = self.ws_class(**workspace_arguments)
    self.controller.parent_controller = parent_controller
    self.max_number_of_steps = nsteps
    self.InitializeCoderack()

  def Run(self):
    self.controller.RunUptoNSteps(self.max_number_of_steps)
