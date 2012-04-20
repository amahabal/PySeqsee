# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

from farg.core.codelet import Codelet
from farg.core.coderack import Coderack
from farg.core.exceptions import StoppingConditionMet
from farg.core.ltm.manager import LTMManager
from farg.core.stream import Stream
from farg.core.util import Toss
from farg.third_party import gflags

FLAGS = gflags.FLAGS

gflags.DEFINE_integer('stopping_condition_granularity', 5,
                      "How frequently the stopping condition is evaluated, as measured in"
                      " number of codelets.")

class Controller(object):
  """A controller is responsible for controlling the Coderack.
     The Coderack, in turn, by the action of codelets, marshals the various pieces of a space
     or of an entire application.  These pieces include the stream, the long-term memory, and
     any pieces added by subclasses (a workspace will typically be added).

     A controller provides the method 'Step'.  This does two things.  First, it may add
     routine codelets.  The controller's constructor specifies what codelets to add and with
     what likelihood.  If the Coderack is empty, the codelets are added regardless of the
     likelihood.  Second, a codelet is selected from the Coderack and executed.  This codelet
     may access the stream, the long-term memory, or the workspace and could even add other
     codelets which the next call to 'Step' may execute.
  """

  #: What type of stream is owned by the controller.
  stream_class = Stream
  #: What type of coderack is owned by the controller.
  coderack_class = Coderack
  #: What type of workspace is owned by the controller. With None, gets no workspace.
  workspace_class = None
  #: This is a list containing 3-tuples made up of (family, urgency, probability).
  #: The probability is ignored during a Step if the coderack is empty.
  routine_codelets_to_add = ()
  #: Name of LTM used by the controller. If None, no LTM is created.
  ltm_name = None

  def __init__(self, *, ui, controller_depth=0,
               parent_controller=None, workspace_arguments=None,
               stopping_condition=None):
    #: How deeply in the stack this controller is. The top-level controller has a depth
    #: of 0, Subspaces it spawns 1, and so forth.
    self.controller_depth = controller_depth
    #: If this is a controller of a subspace, this points to parent_controller.
    self.parent_controller = parent_controller
    #: The coderack.
    self.coderack = self.coderack_class(10)
    #: The stream.
    self.stream = self.stream_class(self)
    if self.workspace_class:
      if workspace_arguments is None:
        workspace_arguments = dict()
      #: Workspace
      self.workspace = self.workspace_class(**workspace_arguments)
    if self.ltm_name:
      #: LTM, if any
      self.ltm = LTMManager.GetLTM(self.ltm_name)
    else:
      self.ltm = None
    #: Number of steps taken
    self.steps_taken = 0
    #: The UI running this controller. May be a GUI or a Guided UI (which knows how to
    #: answer questions that'd normally be answered by a user in a GUI). Any subspace
    #: spawned by this space shall inherit the ui.
    self.ui = ui
    #: Stopping condition (for SxS and batch modes).
    self.stopping_condition = stopping_condition
    # Add any routine codelets...
    self._AddRoutineCodelets(force=True)

  def _AddRoutineCodelets(self, force=False):
    """Add routine codelets to the coderack.

       The codelets are added with a certain probability (specified in the third term of the
       tuple), but this can be over-ridden with force (or if the coderack is empty).

       In the Perl version, this was called 'background codelets'.
    """
    if self.coderack.IsEmpty():
      force = True
    if self.routine_codelets_to_add:
      for family, urgency, probability in self.routine_codelets_to_add:
        if force or Toss(probability):
          self.coderack.AddCodelet(Codelet(family, self, urgency))


  def Step(self):
    """Executes the next (stochastically chosen) step in the model."""
    self.steps_taken += 1
    if self.ltm:
      self.ltm._timesteps = self.steps_taken
    self._AddRoutineCodelets()
    if not self.coderack.IsEmpty():
      codelet = self.coderack.GetCodelet()
      codelet.Run()
    if self.stopping_condition:
      if self.steps_taken % FLAGS.stopping_condition_granularity == 0:
        if self.stopping_condition(self):
          raise StoppingConditionMet(codelet_count=self.steps_taken)

  def RunUptoNSteps(self, n_steps):
    """Takes upto N steps. In these, it is possible that an answer is found and an exception
       raised.
    """
    for _ in range(n_steps):
      if self.ui.pause_stepping:
        return
      self.Step()

  def AddCodelet(self, *, family, urgency, arguments_dict=None):
    """Adds a codelet to the coderack."""
    if arguments_dict is None:
      arguments_dict = {}
    codelet = Codelet(family=family, controller=self,
                      urgency=urgency, arguments_dict=arguments_dict)
    self.coderack.AddCodelet(codelet)
