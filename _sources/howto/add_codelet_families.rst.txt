How to add a new type of codelet
==================================

To define a new type of codelet, a new Codelet Family needs to be created.  To do this, run::

  farg codelet <application name> <codelet name, ex NewCodeletFamily>

This will create a new codelet that looks like this::
  
  class CF_NewCodeletFamily(CodeletFamily):
   '''One line documentation of what codelets of this family do.
    Documentation describes what it does, what codelets it may create, what things
    it may cause to focus on, and any subspace it may be a part of.
    '''

    @classmethod
    def Run(cls, controller, *):
      '''One line documentation of what codelets of this family do.

      Run may take extra arguments (such as other_arg1 above). The extra arguments
      will be passed by name only. These are set in the constructor of the codelet.
      '''
      #TODO: Write out what this codelet does
      
The codelet family above has codelets that take no arguments. To create such
codelets, you will do the following::

  # To create codelet without adding it immediately to any coderack.
  # 20 is the urgency, a number between 0 and 100
  cl = Codelet(CF_NewCodeletFamily, controller, 20)

  # To create and immediately add it to the coderack of a controller:
  controller.AddCodelet(CF_NewCodeletFamily, 20)

To create codelets that take arguments, you will define them like this::

  from farg.core.codelet import CodeletFamily
  class CF_NewCodeletFamily(CodeletFamily):
    @classmethod
    def Run(cls, controller, foo, bar):
      # Do something useful.

Here, the two arguments are 'foo' and 'bar', and both will always be passed by
name. To create codelets::

  cl = Codelet(CF_NewCodeletFamily, controller, 20, dict(foo=3, bar=5))
  controller.AddCodelet(CF_NewCodeletFamily, 20, dict(foo=3, bar=5))

As defined, both arguments are required. If not provided, there will be a run-time
error *when the codelet is run*. To make arguments optional, and do be explicit
about the named-only nature of arguments, you could say::
  
  from farg.core.codelet import CodeletFamily
  class CF_NewCodeletFamily(CodeletFamily):
    @classmethod
    def Run(cls, controller, *, foo, bar=5):
      # Do something useful.
  
Above, 'foo' is required, but 'bar' is optional, defaulting to 5. 

Where to add code
-------------------

The convention is to add code in the codelet_families directory under the app.  This is automatically done when using the farg codelet command.
