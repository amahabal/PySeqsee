from apps.seqsee.util import Toss
from components.coderack import Coderack, CoderackEmptyException
from components.stream import Stream
from farg.codelet import Codelet
import logging

logger = logging.getLogger(__name__)

class Controller(object):
  """The controller of an application (or of a subspace) implements the `Step()` method, which
  takes the next action. It marshals the various pieces --- coderack, stream, workspace, and so
  forth.
  """
  def __init__(self, stream_class=Stream, routine_codelets_to_add=None):
    """This class provides a generic controller. Applications will usually subclass this."""
    #: The coderack. Currently, this always has capacity 10.
    self.coderack = Coderack(10)
    #: The stream.
    self.stream = stream_class(self)
    #: An iterable of three-tuples that names a family, urgency, and probability of addition.
    #: At each step, a codelet is added with the said probability, and with this urgency.
    self.routine_codelets_to_add = routine_codelets_to_add
    #: Number of steps taken
    self.steps_taken = 0

    # Add any routine codelets...
    self._AddRoutineCodelets()

  def _AddRoutineCodelets(self):
    """Add routine codelets to the coderack.
    
    In the Perl version, this was called 'background codelets'.
    """
    if self.routine_codelets_to_add:
      for family, urgency, probability in self.routine_codelets_to_add:
        if Toss(probability):
          self.coderack.AddCodelet(Codelet(family, self, urgency))
        else:
          logging.debug('Skipped adding routine codelet')


  def Step(self):
    """Executes the next (stochastically chosen) step in the model."""
    self.steps_taken += 1
    logger.debug('Started Step #%d', self.steps_taken)
    self._AddRoutineCodelets()
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
