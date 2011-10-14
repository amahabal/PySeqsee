class Controller(object):
  """The controller of an application sits between the UI layer and the runstate.

  The main job of the controller is to implement the `Step()` method, which takes
  the next action.
  """

  def __init__(self, runstate):
    """The controller expects a runstate to be passed to it, which it will own."""
    self.runstate = runstate

  def Step(self):
    """Executes the next (stochastically chosen) step in the model.
    
    Many of the apps using the controller will not need to touch the standard way
    of doing things.
    
    .. Note::
       The default implementation assumes the presence of a coderack and a
       stream, assumptions that hold with the standard RunState class.
    """
    pass


