from farg.codelet import Codelet
from farg.coderack import Coderack
from farg.ltm.manager import LTMManager
from farg.stream import Stream
from farg.util import Toss
import logging

logger = logging.getLogger(__name__)

class Controller(object):
  """A controller is responsible for controlling the Coderack.
     The Coderack, in turn, by the action of codelets, marshals the various pieces of a space
     or of an entire application.  These pieces include the stream, the long-term memory, and
     any pieces added by subclasses (a workspace will typically be added).

     A controller provides the method 'Step'.  This does two things.  First, it may add
     routine codelets.  The controller's constructor specifies what codelets to add and with
     what likelihood.  If the Coderack is empty, the codelets are added regardless of the
     likelihood.  Second, a codelet is selected from the Coderack and executed.  This codelet
     may access the stream, the long-term memory, or the workspace and could even add other
     codelets which the next call to 'Step' may execute.

     Args:
       * stream_class: What sort of stream to set up? Defaults to the standard stream.
       * routine_codelets_to_add: This is a list containing 3-tuples made up of
         (family, urgency, probability). The probability is ignored during a Step if the
         coderack is empty.
       * ltm_name: If provides, the LTM file is loaded and available as self.ltm.
  """
  def __init__(self, stream_class=Stream, routine_codelets_to_add=None, ltm_name=None):
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
    if ltm_name:
      #: The LTM (if any)
      self.ltm = LTMManager.GetLTM(ltm_name)
    else:
      self.ltm = None

    # Add any routine codelets...
    self._AddRoutineCodelets(force=True)

  def _AddRoutineCodelets(self, force=False):
    """Add routine codelets to the coderack.

       The codelets are added with a certain probability (specified in the third term of the
       tuple), but this can be over-ridden with force (or if the coderack is empty).

       In the Perl version, this was called 'background codelets'.
    """
    if self.coderack.IsEmpty():
      force = True
    if self.routine_codelets_to_add:
      for family, urgency, probability in self.routine_codelets_to_add:
        if force or Toss(probability):
          self.coderack.AddCodelet(Codelet(family, self, urgency))
        else:
          logging.debug('Skipped adding routine codelet')


  def Step(self):
    """Executes the next (stochastically chosen) step in the model."""
    self.steps_taken += 1
    if self.ltm:
      self.ltm._timesteps = self.steps_taken
    logger.debug('============ Started Step #%d', self.steps_taken)
    self._AddRoutineCodelets()
    if not self.coderack.IsEmpty():
      codelet = self.coderack.GetCodelet()
      # TODO(#14 --- Dec 28, 2011): Find a way to pretty-print family names.
      logger.debug("Running codelet of family %s", codelet.family)
      codelet.Run()
    else:
      logger.debug("Empty coderack, step is a no-op.")


  def RunUptoNSteps(self, n_steps):
    """Takes upto N steps. In these, it is possible that an answer is found and an exception
       raised.
    """
    for _ in xrange(0, n_steps):
      self.Step()

  def Quit(self):
    """Gets called when the app is about to quit, in case any cleanup is needed."""
    # TODO(# --- Jan 27, 2012): Does not belong here. Just dump current LTM.
    LTMManager.SaveAllOpenLTMS()

  def AddCodelet(self, family, urgency, **arguments):
    """Adds a codelet to the coderack."""
    codelet = Codelet(family, self, urgency, **arguments)
    self.coderack.AddCodelet(codelet)

  def DisplayMessage(self, message):
    if hasattr(self, 'mw'):  # Has the GUI set. O/w, DisplayMessage is a no-op.
      import tkMessageBox
      tkMessageBox.showinfo('', message)
