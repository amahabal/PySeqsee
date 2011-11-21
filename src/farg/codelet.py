"""Base classes for Codelet families and for codelet.

.. ToDo:: Keep eyes open for freshness issues; these have not been ported from Perl.
"""

class CodeletFamily(object):
  pass

class Codelet(object):
  def __init__(self, family, runstate, urgency, **args):
    self.family = family
    self.urgency = urgency
    self.args = args
    self.runstate = runstate

  def Run(self):
    self.runstate.most_recent_codelet = self
    return self.family.Run(self.runstate, **self.args)
