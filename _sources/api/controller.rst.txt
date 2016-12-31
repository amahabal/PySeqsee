Controller
==============
    
A controller is the purely mechanical (read "dumb") loop that controls the
entire application as well as individual subspaces that the application may
create to tackle subproblems. Each subspace gets its own controller.

Each controller has its own coderack, stream, long-term memory, and workspace.
These may be accessed thus, respectively::

  self.coderack
  self.stream
  self.ltm
  self.workspace

Customizing the controller class
---------------------------------

A controller is an instance of a subclass of :py:class:`~farg.core.controller.Controller`. It is
possible to configure the controller in a number of ways. Before we look at the configuration,
here is a brief outline of the main function provided by the controller, namely,
:py:meth:`~farg.core.controller.Controller.Step`.

A step involves choosing a codelet from the coderack and running it. The codelet has access to
each of the components owned by the controller (namely, the coderack, stream, ltm, and
workspace). The action of the codelet can have any number of effects including the creation
of more codelets, directing the application's attention somewhere (a notion explored later
when we look at streams), create structures in the workspace, or extend the LTM or pump
activation into some concept.

Furthermore, after each step, more codelets are probabilistically added to the coderack. The
class variable :py:attr:`~farg.core.controller.Controller.routine_codelets_to_add` contains 3-tuples
(class, urgency, probability) specifying the class of the new codelet, its urgency, and the
probability with which to add it.

In the next few paragraphs, we will look at customizing a hypothetical controller called Foo.
Its code will begin thus::

  class Foo(farg.controller.Controller):
    ...  # customization here

The simplest customization is to specify codelets to be added after each step::

  class Foo(farg.controller.Controller):
    routine_codelets_to_add = ((CodeletFamilyBar, 30, 0.3),
                               (CodeletFamilyBat, 80, 0.2))

Another customization is to use a non-default class for the coderack or the stream. This
should in general not be required, and the default classes :py:class:`~farg.core.coderack.Coderack`
and :py:class:`~farg.core.stream.Stream` should be adequate. But the customization is available if
needed. No argument is passed to the constructor of these classes to create the coderack or
the stream::

  class Foo(farg.controller.Controller):
    self.coderack_class = SomeClass
    self.stream_class = SomeOtherClass

The workspace class can be specified as follows. If it is not Null, it will be
initialized with a dictionary that is passed in the workspace_arguments argument
of the controller's constructor::

  self.workspace_class = YetAnotherClass  # Default: None

The LTM's name can be specified as below. The LTM manager will be used to load
this (if not already loaded) and to initialize it if it is empty::

  self.ltm_name = 'LtmName'  # Default: None

The UI
--------

A UI can be graphical or not. At any time, at most one UI is active, and it is
shared by all controllers. It can be accessed as::
  
  self.ui  # Points to the UI (usually a GUI).

The UI provides the important method called :py:meth:`~farg.core.ui.gui.GUI.AskQuestion`. This can be
used by the controller to ask for confirmation of the answer, for instance. In case of a
graphical UI, this could result in the user being asked the question. In other
cases (such as in automated testing), the UI may be given enough knowledge to
answer the question itself. See the UI documentation for details.

The Stopping Condition
------------------------

It is possible to specify a stopping condition for a controller. This is useful for testing
when weighing a potential change. When contemplating the change, it is useful to see how long
it takes with the change and without the change until some significant event occurs (such as
the discovery of the answer, for instance). This will be discussed elsewhere.

The Constructor
---------------- 

The constructor takes the following named arguments:

  * ui (required)
  * controller_depth. The top controller has depth 0, its subspaces have depth 1, and so
    forth. The default is 0.
  * parent_controller. If present, it points to the controller that created this subspace.
    Defaults to None (which indicates a top-level controller).
  * workspace_arguments. If present, this should be a dict() and will be used to initialize
    the workspace.
  * stopping_condition. If present, this should be a function that takes the controller as
    the only input and returns true or false.

Available attributes and methods
----------------------------------

  * The epoch of the controller --- how many steps it has taken --- is
    maintained::

     self.steps_taken 

  * This is a utility to add a codelet. This is needed since every codelet
    keeps a pointer to a controller::

      self.AddCodelet(family, urgency, dict(arg1=3, arg2=5))

  * Finally, it provides a Step method. It executes the next (stochastically
    chosen) step in the model::

      self.Step()
