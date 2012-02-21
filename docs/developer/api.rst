APIs for the Core
=================

The User Interface
---------------------

The base class of the user interface is *farg/ui*. Subclasses should support the
following.

  * It should hold a controller object::

      self.controller  # Holds the controller object.

  * The contoller can be stepped through::

      self.controller.Step(7)  # Step the controller 7 steps.

  * Some UI initializations (such as a GUI) may do some setup/teardown. They
    should override these methods::

      self.Setup()  # Defaults to a no-op.
      self.Teardown()  # Defaults to a no-op.

  * The UI must deal with displaying messages and asking questions to the user.
    In some cases, these methods would be overridden to automatically answer
    such questions (in a testing suite, for example). The code calling these 
    functions should not care about who is answering them::

      self.DisplayMessage()  # In a GUI, will display the message in a pop-up.
      is_palindrome = self.AskYesNoQuestion("Is this a palindrome?")

    .. note::

      Not designed yet: A way to ask more complex questions that an app developed
      using this framework may support.
    
Controller
------------
    
The controller marshalls the various pieces such as coderack, stream and the
workspace.
    
  * Keeps a pointer to the UI. Subspaces have their own contollers, but they
    all point to the same UI. This is needed for such tasks as asking a
    question::
    
      self.ui  # Points to the UI (usually a GUI).
      
  * Keeps a pointer to a coderack::
  
      self.coderack  # Created when controller is initialized
     
  * Keeps a pointer to a stream. This stream is of the class specified at
    construction::
    
      self.stream
      
  * Keeps a pointer to an LTM. This can be *None*::
  
      self.ltm
      
  * It is possible to ask the controller to add certain codelets at each step.
    This is specified at construction using an iterable consisting of any
    number of 3-tuples (family, urgency, probability-of-addition)::
    
     self.routine_codelets_to_add

  * The constructor becomes clearer in terms of the bullets above. The
    *stream_class* controls the type of stream created, the 
    *routine_codelets_to_add* controls codelets added at each stage, and
    *ltm_name* helps choose which LTM to load, if any::

      c = Controller(stream_class=Stream,
                     routine_codelets_to_add=None,
                     ltm_name=None)
  
     
  * The epoch of the controller --- how many steps it has taken --- is
    maintained::
     
     self.steps_taken 

  * This is a utility to add a codelet. This is needed since every codelet
    keeps a pointer to a controller::

      self.AddCodelet(family, urgency, dict(arg1=3, arg2=5))

  * Finally, it provides a Step method. It executes the next (stochastically
    chosen) step in the model.

    This should catch all farg-related exceptions and prevent them from
    bubbling to the UI::

      self.Step()
