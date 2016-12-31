Codelet
==========

A codelet is a unit of action in Seqsee. A codelet belongs to a codelet family which
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

* Stores a reference to the controller, family, urgency, and the arguments supplied at the
  time of construction::
    
      self.family
      self.urgency
      self.args
      self.controller
      
* Run causes the codelet to be executed by calling the Run method of the family::
  
    self.Run()