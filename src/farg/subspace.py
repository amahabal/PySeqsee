from farg.controller import Controller
from farg.meta import SubspaceMeta

class Subspace(metaclass=SubspaceMeta):
  controller_class = Controller

  @staticmethod
  def QuickReconn(**args):
    raise Exception("Attempt to call Subspace(). Surely you meant to call a subclass?")

  def InitializeCoderack(self):
    raise Exception("Base InitializeCoderack called. This should have been overridden "
                    "(to set up the initial codelet, for example)")

  def RoutineCodeletsToAdd(self):
    return None

  def __init__(self, parent_controller, nsteps, workspace_arguments):
    self.controller = self.controller_class(
        ui=parent_controller.ui,
        state_lock=None,
        controller_depth=(parent_controller.controller_depth + 1),
        workspace_arguments=workspace_arguments,
        parent_controller=parent_controller)
    self.max_number_of_steps = nsteps
    self.InitializeCoderack()

  def Run(self):
    self.controller.RunUptoNSteps(self.max_number_of_steps)
