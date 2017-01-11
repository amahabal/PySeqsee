import logging

from farg.core.codelet import CodeletFamily

#This class will be filled up with codelets.
#To create a codelet, run "farg codlet {application_name} <codelet name>"

class CF_Detectsimilarity(CodeletFamily):
   '''One line documentation of what codelets of this family do.
    Documentation describes what it does, what codelets it may create, what things
    it may cause to focus on, and any subspace it may be a part of.
    '''

    @classmethod
    def Run(self, controller, *, other_arg1, other_arg2):
      '''One line documentation of what codelets of this family do.

      Run may take extra arguments (such as other_arg1 above). The extra arguments
      will be passed by name only. These are set in the constructor of the codelet.
      '''
      #TODO: Write out what this codelet does

class CF_Findcenter(CodeletFamily):
   '''One line documentation of what codelets of this family do.
    Documentation describes what it does, what codelets it may create, what things
    it may cause to focus on, and any subspace it may be a part of.
    '''

    @classmethod
    def Run(self, controller, *, other_arg1, other_arg2):
      '''One line documentation of what codelets of this family do.

      Run may take extra arguments (such as other_arg1 above). The extra arguments
      will be passed by name only. These are set in the constructor of the codelet.
      '''
      #TODO: Write out what this codelet does
