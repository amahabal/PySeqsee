"""Base classes for Codelet families and for codelet."""
class CodeletFamily(object):
  pass

class Codelet(object):
  def __init__(self, family, runstate, urgency, **args):
    self.family = family
    self.urgency = urgency
    self.args = args
    self.runstate = runstate

  def Run(self):
    return self.family.Run(self.runstate, **self.args)
