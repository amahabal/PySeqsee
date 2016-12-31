Codelet Family
==================

 A codelet family is a class that defines what happens when you run a codelet of that
 family.
 
 Codelet family names typically start with CF.
 
 A codelet family subclasses this class and looks like this::
 
   class CF_Foo(CodeletFamily):
     "Documentation describes what it does, what codelets it may create, what things
      it may cause to focus on, and any subspace it may be a part of.
     "
     
     Name = "Foo"
     
     @classmethod
     def Run(self, controller, other_arg1, other_arg2):
       "Run may take extra arguments (such as other_arg1 above). The extra arguments
        will be passed by name only. These are set in the constructor of the codelet.
       "
       DoSomething()

