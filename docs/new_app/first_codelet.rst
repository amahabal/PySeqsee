Creating the first codelet
============================

In the interest of pedagogy, we will cheat. Our first codelet will be a clunky piece of code that
checks whether the answer "Odd numbers on left, even on right" works, and then reports this to the
user. We wll name this codelet CF_HorribleHack. The prefix 'CF' stands for "Codelet Family".

The farg command can be used here::

  farg codelet bongard HorribleHack

.. note::

  The prefix CF is automatically added.


The new class looks thus::

  class CF_HorribleHack(CodeletFamily):
    @classmethod
    def Run(cls, controller, *):
      pass

Now update it to check for odd/even and just display the answer::

  class CF_HorribleHack(CodeletFamily):
    '''Checks if the solution is odd/even.
  
       This is here merely for demonstration purposes. See :doc:`new_app/first_codelet` for details.
    '''
      @classmethod
      def Run(cls, controller):
        '''Check if solution is even/odd.'''
        workspace = controller.workspace
        if (all(x.magnitude % 2 == 1 for x in workspace.left_items) and
            all(x.magnitude % 2 == 0 for x in workspace.right_items)):
          controller.ui.DisplayMessage("This is an odd/even split")
        else:
          controller.ui.DisplayMessage("I have no idea what this sequence is")

Getting the codelet to run
------------------------------

We will need to tell the controller to run this codelet. Let's edit farg/apps/bongard/controller.py.
We will add the codelet in the init function::

  class BongardController(Controller):
    def __init__(self, **args):
      # Existing code

      # Add this at the end.
      from farg.apps.bongard.codelet_families.all import CF_HorribleHack
      self.AddCodelet(family=CF_HorribleHack, urgency=100)

Run the app
-------------

When you run the app now with 'farg run bongard ---left 1 3 7 ---right 2 4 6', a GUI shows up with the
items visible on screen. Pressing 's' for 'Step' at this point runs one codelet, and it will be the
codelet we just added, which will print an answer to the screen.

.. note::

  The UI supports a few key bindings:
  
  * 'q' for Quit
  * 'c' for Continue (full-steam ahead!)
  * 'p' for Pause while running
  * 's' for Step (run one codelet)
  * 'l' for taking a 10-codelet stride
  * 'k' for taking a 100-codelet stride.