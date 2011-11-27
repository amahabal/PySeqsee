from components.coderack import Coderack, CoderackEmptyException
from components.stream import Stream
from farg.codelet import Codelet
from apps.seqsee.util import Toss

import logging
logger = logging.getLogger(__name__)

class Controller(object):
  """The controller of an application (or of a subspace) implements the `Step()` method, which
  takes the next action. It marshals the various pieces --- coderack, stream, workspace, and so
  forth.
  """
  def __init__(self):
    """This class provides a generic controller. Applications will usually subclass this."""
    #: The coderack. Currently, this always has capacity 10.
    self.coderack = Coderack(10)
    #: The stream. This is a generic structure, and should not need to be subclassed. If
    #: subclassing turns out to be a big need, then this way of initialization will need to be
    #: diddled.
    self.stream = Stream()
    #: An iterable of three-tuples that names a family, urgency, and probability of addition.
    #: At each step, a codelet is added with the said probability, and with this urgency.
    self.routine_codelets_to_add = None

  def Step(self):
    """Executes the next (stochastically chosen) step in the model."""
    if self.routine_codelets_to_add:
      for family, urgency, probability in self.routine_codelets_to_add:
        if Toss(probability):
          self.coderack.AddCodelet(Codelet(family, self, urgency))
    if not self.coderack.IsEmpty():
      codelet = self.coderack.GetCodelet()
      logger.debug("Running codelet of family %s", codelet.family)
      codelet.Run()
    else:
      logger.debug("Empty coderack, step is a no-op.")


  def RunUptoNSteps(self, n_steps):
    """Takes upto N steps. In these, it is possible that an answer is found and an exception
    raised."""
    for n in xrange(0, n_steps):
      self.Step()

  def Quit(self):
    """Gets called when the app is about to quit, in case any cleanup is needed."""
    pass

  def AddCodelet(self, family, urgency, **arguments):
    """Adds a codelet to the coderack."""
    codelet = Codelet(family, self, urgency, **arguments)
    self.coderack.AddCodelet(codelet)
