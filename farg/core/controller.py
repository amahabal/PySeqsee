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

"""This file defines the core controller."""

import logging

from farg.core.codelet import Codelet
from farg.core.coderack import Coderack
from farg.core.exceptions import StoppingConditionMet
from farg.core.history import History, EventType, ObjectType
from farg.core.ltm.manager import LTMManager
from farg.core.stream import Stream
from farg.core.util import Toss

import farg_flags

class Controller:
  """Purely mechanical (read "dumb") loop to control entire app or individual subspaces.

  Each subspace gets its own controller.

  Each controller has its own coderack, stream, long-term memory, and workspace. These may be
  accessed thus, respectively::

      self.coderack
      self.stream
      self.ltm
      self.workspace

  **Customizing the controller class**

  A controller is an instance of a subclass of :py:class:`~farg.core.controller.Controller`.
  It is possible to configure the controller in a number of ways. Before we look at the
  configuration, here is a brief outline of the main function provided by the controller,
  namely, :py:meth:`~farg.core.controller.Controller.Step`.

  A step involves choosing a codelet from the coderack and running it. The codelet has access
  to each of the components owned by the controller (namely, the coderack, stream, ltm, and
  workspace). The action of the codelet can have any number of effects including the creation
  of more codelets, directing the application's attention somewhere (a notion explored later
  when we look at streams), create structures in the workspace, or extend the LTM or pump
  activation into some concept.

  Furthermore, after each step, more codelets are probabilistically added to the coderack.
  The class variable :py:attr:`~farg.core.controller.Controller.routine_codelets_to_add`
  contains 3-tuples (class, urgency, probability) specifying the class of the new codelet,
  its urgency, and the probability with which to add it.

  In the next few paragraphs, we will look at customizing a hypothetical controller called
  Foo. Its code will begin thus::

    class Foo(farg.controller.Controller):
      ...  # customization here

  The simplest customization is to specify codelets to be added after each step::

    class Foo(farg.controller.Controller):
      routine_codelets_to_add = ((CodeletFamilyBar, 30, 0.3),  # 30 is the urgency, 0.3 probability of adding.
                                 (CodeletFamilyBat, 80, 0.2))

  Another customization is to use a non-default class for the coderack or the stream. This
  should in general not be required, and the default classes
  :py:class:`~farg.core.coderack.Coderack` and :py:class:`~farg.core.stream.Stream` should be
  adequate. But the customization is available if needed. No argument is passed to the
  constructor of these classes to create the coderack or the stream::

    class Foo(farg.controller.Controller):
      self.coderack_class = SomeClass
      self.stream_class = SomeOtherClass

  The workspace class can be specified as follows. If it is not Null, it will be initialized
  with a dictionary that is passed in the workspace_arguments argument of the controller's
  constructor::

    self.workspace_class = YetAnotherClass  # Default: None

  The LTM's name can be specified as below. The LTM manager will be used to load this (if not
  already loaded) and to initialize it if it is empty::

    self.ltm_name = 'LtmName'  # Default: None

  **The UI**

  A UI can be graphical or not. At any time, at most one UI is active, and it is shared by
  all controllers. It can be accessed as::

    self.ui  # Points to the UI (usually a GUI).

  The UI provides the important method called :py:meth:`~farg.core.ui.gui.GUI.AskQuestion`.
  This can be used by the controller to ask for confirmation of the answer, for instance. In
  case of a graphical UI, this could result in the user being asked the question. In other
  cases (such as in automated testing), the UI may be given enough knowledge to answer the
  question itself. See the UI documentation for details.

  **The Stopping Condition**

  It is possible to specify a stopping condition for a controller. This is useful for testing
  when weighing a potential change. When contemplating the change, it is useful to see how
  long it takes with the change and without the change until some significant event occurs
  (such as the discovery of the answer, for instance). This will be discussed elsewhere.

  **The Constructor**

  The constructor takes the following named arguments:

    * ui (required)
    * controller_depth. The top controller has depth 0, its subspaces have
      depth 1, and so forth. The default is 0.
    * parent_controller. If present, it points to the controller that created this
      subspace. Defaults to None (which indicates a top-level controller).
    * workspace_arguments. If present, this should be a dict() and will be used to
      initialize the workspace.
    * stopping_condition. If present, this should be a function that takes the controller
      as the only input and returns true or false.
  """
  #: What type of stream is owned by the controller. Defaults to
  #: :py:class:`~farg.core.stream.Stream`
  stream_class = Stream  # This is not "constant" as thought by pylint: disable=C6409
  #: What type of coderack is owned by the controller. Defaults to
  #: :py:class:`~farg.core.coderack.Coderack`.
  coderack_class = Coderack  # pylint: disable=C6409
  #: What type of workspace is owned by the controller. With None, gets no workspace.
  workspace_class = None   # pylint: disable=C6409
  #: This is a list containing 3-tuples made up of (family, urgency, probability).
  #: The probability is ignored during a Step if the coderack is empty.
  routine_codelets_to_add = ()  # pylint: disable=C6409
  #: Name of LTM used by the controller. If None, no LTM is created.
  ltm_name = None   # pylint: disable=C6409

  def __init__(self, *, ui, controller_depth=0,
               parent_controller=None, workspace_arguments=None,
               stopping_condition=None):
    History.AddArtefact(self, ObjectType.CONTROLLER, "Created controller")
    #: How deeply in the stack this controller is. The top-level controller has a depth
    #: of 0, Subspaces it spawns 1, and so forth.
    self.controller_depth = controller_depth
    #: If this is a controller of a subspace, this points to parent_controller.
    self.parent_controller = parent_controller
    #: The coderack.
    self.coderack = self.coderack_class()
    #: The stream.
    self.stream = self.stream_class(self)
    if self.workspace_class:
      if workspace_arguments is None:
        workspace_arguments = dict()
      #: Workspace, constructed if workspace_class is defined. The workspace is constructed
      #: using workspace_arguments.
      self.workspace = self.workspace_class(**workspace_arguments)  # pylint: disable=E1102
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

    The codelets are found in routine_codelets_to_add, which is a list of 3-tuples. Each
    3-tuple contains the codelet family, urgency, and probability with which to add that
    codelet.

    Args:
      force:
        If true, the third field of the 3-tuple ("probability of adding") is ignored.

    The codelets are added with a certain probability (specified in the third term of the
    tuple), but this can be over-ridden with force (or if the coderack is empty).
    """
    if self.coderack.IsEmpty():
      force = True
    if self.routine_codelets_to_add:
      for family, urgency, probability in self.routine_codelets_to_add:
        if force or Toss(probability):
          cl = Codelet(family, self, urgency)
          self.coderack.AddCodelet(cl, msg="Routine codelet")

  def Step(self):
    """Executes the next (stochastically chosen) step in the model."""
    self.steps_taken += 1
    if self.ltm:
      self.ltm._timesteps = self.steps_taken
    self._AddRoutineCodelets()
    if not self.coderack.IsEmpty():
      codelet = self.coderack.GetCodelet()
      History.AddEvent(EventType.CODELET_RUN_START,
                       "Codelet run started", [[codelet, ""]])
      codelet.Run()
    if self.stopping_condition:
      if self.steps_taken % farg_flags.FargFlags.stopping_condition_granularity == 0:
        if self.stopping_condition(self):
          raise StoppingConditionMet(codelet_count=self.steps_taken)

  def RunUptoNSteps(self, n_steps):
    """Takes up to N steps.

    Args:
      n_steps:
        Number of steps to take. Steps taken by subspaces created by this controller
        are not counted.

    In these, it is possible that an answer is found and an exception raised.
    """
    for _ in range(n_steps):
      if self.ui.pause_stepping:
        return
      self.Step()

  def AddCodelet(self, *, family, urgency, arguments_dict=None, parents=None, msg=""):
    """Adds a codelet to the coderack.

    Keyword-only Args:
      family:
        Family of codelet. Subclass of :py:class:`~farg.core.codelet.CodeletFamily`.
      urgency:
        Number between 0 and 100 indicating urgency.
      arguments_dict:
        A dictionary of extra arguments to pass to the codelet. See details in the
        documentation of :py:class:`~farg.core.codelet.CodeletFamily`.
    """
    if arguments_dict is None:
      arguments_dict = {}
    codelet = Codelet(family=family, controller=self,
                      urgency=urgency, arguments_dict=arguments_dict)
    self.coderack.AddCodelet(codelet, parents=parents, msg=msg)

  def SendActivation(self, *, content, amount):
    """Sends activation to content in LTM."""
    self.ltm.GetNode(content=content).IncreaseActivation(amount, current_time=self.steps_taken)

  def GetActivation(self, *, content):
    """Gets the activation from the LTM."""
    return self.ltm.GetNode(content=content).GetActivation(current_time=self.steps_taken)
