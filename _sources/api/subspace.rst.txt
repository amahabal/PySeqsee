Subspace
=============

A subspace is created for a specific task (think "explaining an answer" or "estimating if
we have solved the problem".

:py:class:`farg.subspace.Subspace` is the base class from which any particular subspace
is derived. To create a new type of subspace, we subclass like this::

  class SubspaceFoo(Subspace):
     """This subspace does Foo."""
     pass  # More details below

In order to use the subspace, you will say elsewhere::

  response = SubspaceFoo(controller, workspace_arguments=dict(x=3)).Run()

This has the following effect, in this order:

1. If the class defines a method QuickReconn, it is called. It will try to do a quick and
   superficial job of completing the task. This returns a QuickReconnResponse object, which
   can be one of three things:
  
   * An indication that an answer has been found
   * An indication that the superficial exploration showed that no answer will be found
   * A request for deeper exploration. Deeper exploration involves a system very similar to
     the system for the entire application --- that is, a controller, stream, coderack, ltm,
     and workspace will be setup, and multiple codelets will attempt to reach an answer.

   If it is one of the first two responses, either the answer or `None` is returned, as
   appropriate. Otherwise, the extra machinery of controller and so forth is set up.

2. The InitializeCoderack method is called. If there is any chance that the QuickReconn
   method will return the third response (deeper exploration), this method must be
   defined. This will add one or more codelets to the coderack.
  
3. The controller is started. Its codelets can raise `AnswerFound` or `NoAnswerCanBeFound`
   exceptions to return an answer. If the maximum number of allowed codelets is reached
   without either exception, `None` is returned.

QuickReconn
-------------

This method has access to the parent controller (and therefore its workspace and other pieces),
to the workspace arguments passed in, and the number of steps allowed for the controller::

  self.parent_controller
  self.workspace_arguments:
  self.nsteps

Initializing the Coderack
---------------------------

When InitializeCoderack is called, the controller has already been set up. A typical
initialization function looks like::

  def InitializeCoderack(self):
    self.controller.AddCodelet(SomeCodeletFamily, urgency=10, arguments=dict()) 
