"""BatchUI contains code to handle questions that would a user would in GUI.

When run in GUI-mode, a PySeqsee application is interactive and may ask the
user questions (e.g., "Are the next three terms 2, 3, and 5?"). To facilitate
running in batch mode multiple times, a "simulated user" will need to answer
these questions.

To do this, you may perhaps pass an extra flag to the program revealing the
answer in some way (e.g., in Seqsee, the next few terms can be revealed in
order to automatically answer questions such as the one above.).
"""

from farg.core.ui.batch_ui import BatchUI

# If you need access to flags, you need:
# import farg_flags
# # The flag --foo is available at farg_flags.FargFlags.foo

class BongardBatchUI(BatchUI):
  """Simulated user to answer questions that a user would in GUI."""

  def RegisterQuestionHandlers(self):
    """Registers handlers for various questions."""
    pass
