Subspace
=============

This is the base class from which subspace classes subclass. To call a subspace --- say,
SubspaceFoo --- just construct a subclass object, and it will take care of the rest::

    return_value = SubspaceFoo(parent_controller, nsteps=5,
                               args=dict(a=3, b=5))

The subclass should define a method that will do a quick survey over available methods
to come up with a quick solution or a recommendation for deeper exploration::
 
    class SubspaceFoo(Subspace):
      ...
      @staticmethod
      def QuickReconn(arg1, arg2):
        # do something. 