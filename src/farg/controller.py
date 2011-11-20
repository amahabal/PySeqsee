from components.coderack import Coderack, CoderackEmptyException
from components.stream import Stream
from farg.codelet import Codelet
from apps.seqsee.util import Toss

class Controller(object):
  """The controller of an application sits between the UI layer and the runstate.

  The main job of the controller is to implement the `Step()` method, which takes
  the next action.
  """

  def __init__(self, runstate):
    """The controller expects a runstate to be passed to it, which it will own."""
    self.runstate = runstate
    self.coderack = Coderack(10)
    self.stream = Stream()
    #: An iterable of three-tuples that names a family, urgency, and probability of addition.
    #: At each step, a codelet is added with the said probability, and with this urgency.
    self.routine_codelets_to_add = None

  def Step(self):
    """Executes the next (stochastically chosen) step in the model.
    
    Many of the apps using the controller will not need to touch the standard way
    of doing things.
    
    .. Note::
       The default implementation assumes the presence of a coderack and a
       stream, assumptions that hold with the standard RunState class.
    """
    if self.routine_codelets_to_add:
      for family, urgency, probability in self.routine_codelets_to_add:
        if Toss(probability):
          self.coderack.AddCodelet(Codelet(family, self.runstate, urgency))
    if not self.coderack.IsEmpty():
      codelet = self.coderack.GetCodelet()
      codelet.Run()

  def RunUptoNSteps(self, n_steps):
    """Takes upto N steps. In these, it is possible that an answer is found and an exception
    raised."""
    for n in xrange(0, n_steps):
      self.Step()

  def Quit(self):
    """Gets called when the app is about to quit, in case any cleanup is needed."""
    pass

