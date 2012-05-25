# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

"""Classes defining a Codelet and the base class for all Codelet families."""

from abc import ABCMeta, abstractmethod

class CodeletFamily(metaclass=ABCMeta):
  """A codelet family is a class that defines what happens when you run a codelet of that
     family.
     
     Codelet family names typically start with CF.
     
     A codelet family subclasses this class and looks like this::

       from farg.core.codelet import CodeletFamily     
       class CF_Foo(CodeletFamily):
         "Documentation describes what it does, what codelets it may create, what things
          it may cause to focus on, and any subspace it may be a part of.
         "
         
         @classmethod
         def Run(self, controller, *, other_arg1, other_arg2):
           "Run may take extra arguments (such as other_arg1 above). The extra arguments
            will be passed by name only. These are set in the constructor of the codelet.
           "
           DoSomething()
  """

  @abstractmethod
  def Run(self, controller):
    """Runs the codelet. Subclasses should overrride this, and arrange to handle any specific
       arguments it needs. These arguments are guaranteed to be passed in as keyword
       arguments.
    """
    pass

class Codelet(object):
  """A codelet is a unit of action in Seqsee. A codelet belongs to a codelet family which
     defines what it does. The codelet has an urgency that controls how likely the codelet
     is to run (based on the urgency of other codelets waiting to run), and it has a
     dictionary of arguments that will be used when running the codelet (if ever).

     If extra arguments are passed while constructing the codelet, the Run() method of the
     codelet family must be capable of handling these. 
     
     There are two ways of constructing. The first creates the codelet but does not yet
     place it on the coderack::
     
       c = Codelet(family, controller, urgency, dict(other_arg=10, other_arg2=15))
       
     The second method is to call AddCodelet on the controller::
     
       controller.AddCodelet(family, urgency, dict(other_arg=10, other_arg2=15))
  """
  def __init__(self, family, controller, urgency, arguments_dict=None):
    self.family = family
    self.urgency = urgency
    self.args = arguments_dict if arguments_dict is not None else {}
    self.controller = controller

  def Run(self):
    """Runs the codelet."""
    self.controller.most_recent_codelet = self
    return self.family.Run(self.controller, **self.args)
