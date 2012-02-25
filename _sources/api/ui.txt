The User Interface
====================

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

