"""Base classes for Codelet families and for codelet.

.. ToDo:: Keep eyes open for freshness issues; these have not been ported from Perl.
"""

class CodeletFamily(object):
  # TODO(#9 --- Dec 28, 2011): Add documentation.
  pass

class Codelet(object):
  # TODO(#10 --- Dec 28, 2011): Add documentation.
  def __init__(self, family, controller, urgency, **args):
    self.family = family
    self.urgency = urgency
    self.args = args
    self.controller = controller

  def Run(self):
    self.controller.most_recent_codelet = self
    return self.family.Run(self.controller, **self.args)
