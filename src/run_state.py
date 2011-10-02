from coderack import Coderack 
class RunState(object):
  """Maintains the state of the current run.
  
  Such information as number of codelets run, the current coderack, etc. belong
  here.
  
  (Anything in Globals.pm previously should end up here).
  """

  def __init__(self, arguments):
    """Initialize a fresh run.
    
    args:
      arguments: An object created from the command-line. This may have been
        sligtly modified depending on ui (batch may be different from gui, for
        instance, but perhaps not!).
    """
    
    revealed_terms = arguments.sequence
    
    all_terms = revealed_terms
    all_terms.extend(arguments.unrevealed_terms)

    self.codelets_run = 0
    
    # Terms of "real" sequence. Seqsee may be unaware of some of these.
    self.real_sequence = all_terms
    self.coderack = Coderack(arguments.coderack_size)
    