Setting up Workspace
=======================

Next, we will set up the workspace and the display of the workspace.

Remember that we have, at this stage, the following constructor for the workspace::

  def __init__(self, *, left_integers, right_integers):
    pass

We will now store these inputs, but first we will create objects from them. We
will not use mere integers because we want to store extra information (such as the
fact that a particular value is a prime number). Let's first add a class to the
workspace file. A simple class suffices for now. We will make this more elaborate
later::

  class Element:
    """Class to store individual elements of the left and right sets."""
    def __init__(self, magnitude):
      self.magnitude = magnitude

And the workspace constructor itself is changed to::

  def __init__(self, *, left_integers, right_integers):
    self.left_integers = [Element(x) for x in left_integers]
    self.right_integers = [Element(x) for x in right_integers]

Updating the UI
-----------------

For now, the UI display of the workspace can be simple. We will modify the ReDrawView
function in 'farg/apps/numeric_bongard/gui/workspace_view.py', which currently is::

  def ReDrawView(self, controller):
    """Redraw the workspace if it is being displayed. This is not called otherwise.

    The attributes that you have access to include self.width, self.height and a method to
    convert this widget's coordinates to the full canvas coordinates.
    """
    workspace = controller.workspace

    # EDIT-ME: You'd want to add something real here.
    x, y = self.CanvasCoordinates(10, 10)
    self.canvas.create_text(x, y, text='Hello, World!', anchor=NW)

After modification, it will be::

  def ReDrawView(self, controller):
    """Redraw the workspace if it is being displayed. This is not called otherwise.

    The attributes that you have access to include self.width, self.height and a method to
    convert this widget's coordinates to the full canvas coordinates.
    """
    workspace = controller.workspace

    x_for_left = 5
    x_for_right = 5 + self.width / 2
    y_delta_for_left = (self.height - 10) / len(workspace.left_integers)
    y_delta_for_right = (self.height - 10) / len(workspace.right_integers)

    for i, element in enumerate(workspace.left_integers):
      x, y = self.CanvasCoordinates(x_for_left, 5 + i * y_delta_for_left)
      self.canvas.create_text(x, y, text=str(element.magnitude), anchor=NW)

    for i, element in enumerate(workspace.right_integers):
      x, y = self.CanvasCoordinates(x_for_right, 5 + i * y_delta_for_right)
      self.canvas.create_text(x, y, text=str(element.magnitude), anchor=NW)

And that's it. So now we have a rudimentary way to display the WS. 
