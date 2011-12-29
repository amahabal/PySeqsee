"""Base classes for Codelet families and for codelet.

.. ToDo:: Keep eyes open for freshness issues; these have not been ported from Perl.
"""

class CodeletFamily(object):
  """A codelet family is a class that defines what happens when you run a codelet of that
     family.
     
     Naming:
     --------
     
     Codelet family names typically start with CF_.
     
     Interface:
     -----------
     A codelet family subclasses this class and looks like this::
     
       class CF_Foo(CodeletFamily):
         "Documentation describes what it does, what codelets it may create, what things
          it may cause to focus on, and any subspace it may be a part of.
         "
         
         @classmethod
         def Run(self, controller, other_arg1, other_arg2):
           "The extra arguments will be passed by name only."
           DoSomething()
  """
  pass

class Codelet(object):
  """A codelet is a unit of action in Seqsee. A codelet belongs to a codelet family which
     defines what it does. The codelet has an urgency that controls how likely the codelet
     is to run (based on the urgency of other codelets waiting to run), and it has a
     dictionary of arguments that will be used when running the codelet (if ever).
     
     Construction:
     --------------
     
     There are two ways of constructing. The first creates the codelet but does not yet
     place it on the coderack::
     
       c = Codelet(family, controller, urgency, other_arg=10, other_arg2=15)
       
     The second method is to call AddCodelet on the controller::
     
       controller.AddCodelet(family, urgency, other_arg=10, other_arg2=15)
  """
  def __init__(self, family, controller, urgency, **args):
    self.family = family
    self.urgency = urgency
    self.args = args
    self.controller = controller

  def Run(self):
    self.controller.most_recent_codelet = self
    return self.family.Run(self.controller, **self.args)
