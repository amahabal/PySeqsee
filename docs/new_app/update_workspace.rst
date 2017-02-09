Update Workspace
====================

The workspace is the "working memory" of the app, and we will need to update it to contain our two
sets. Let's update farg/apps/bongard/workspace.py.

First, we will create a class that will hold our numbers from each set. We will later extend this
class significantly (and add super classes that enable this to have categories, be in the stream, be
part of the long-term memory, and so forth), but for now keep it simple::

  class IntegerObject(object):
    """Holds one item in either set, along with any book-keeping information."""

    def __init__(self, magnitude):
      self.magnitude = magnitude

The BongardWorkspace class there is nearly empty. Let the constructor know that we will have a left
set and a right set. For convenience, we will keep these lists rather than sets::

  class BongardWorkspace:
    def __init__(self):
      self.left_items = []
      self.right_items = []

Finally, we will add a method to set these values::

  class BongardWorkspace:
    def SetItems(self, left_magnitudes, right_magnitudes):
      for magnitude in left_magnitudes:
        self.left_items.append(IntegerObject(magnitude))
      for magnitude in right_magnitudes:
        self.right_items.append(IntegerObject(magnitude))

Update Controller
==================

The Workspace is owned by a controller (which also owns the other resources such as the stream), and
the controller is the one that sets up the workspace initially. So we should update it in the file
farg/apps/bongard/controller.py.

This is how the BongardController class currently looks::

  class BongardController(Controller):
    """Controller for Bongard."""
    # EDIT-ME: possibly set up routine_codelets_to_add.
    workspace_class = BongardWorkspace
    ltm_name = kLTMName
  
    def __init__(self, **args):
      Controller.__init__(self, **args)
      
We will make a couple of changes for now. First, we will make the flags accessible from this file::

  import farg.flags as farg_flags
  
And we will update the workspace with the relevant inputs::

  class BongardController(Controller):
    def __init__(self, **args):
      Controller.__init__(self, **args)
      self.workspace.SetItems(farg_flags.FargFlags.left, farg_flags.FargFlags.right)
