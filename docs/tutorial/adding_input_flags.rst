Adding Input Flags
===================

Here, we will create the flags '--left' and ''-right' for the inputs. To do this,
we will define the flags in the file 'farg/apps/numeric_bongard/run_numeric_bongard.py'.
That file already defines the flag '--input', and we will replace this line with::

  gflags.DEFINE_string('left_input', '',
                       'Comma-separated list of numbers on the left side.')
  gflags.DEFINE_string('right_input', '',
                       'Comma-separated list of numbers on the right side.')

We will need to arrange for these to be passed on to the workspace. To do so,
we modify the __init__ method of the controller in the file
'farg/apps/numeric_bongard/controller.py'. When we start, this method just passes
the buck to the constructor of its base class and looks like this::

  def __init__(self, *, ui, controller_depth=0,
               parent_controller=None, workspace_arguments=None,
               stopping_condition=None):
    Controller.__init__(self, ui=ui, parent_controller=parent_controller,
                        workspace_arguments=workspace_arguments,
                        stopping_condition=stopping_condition)

After modification it looks like this::

  def __init__(self, *, ui, controller_depth=0,
               parent_controller=None, workspace_arguments=None,
               stopping_condition=None):
    left_integers = FLAGS.left_input.split()
    right_integers = FLAGS.right_input.split()
    workspace_arguments = dict(left_integers=left_integers,
                               right_integers=right_integers)
    Controller.__init__(self, ui=ui, parent_controller=parent_controller,
                        workspace_arguments=workspace_arguments,
                        stopping_condition=stopping_condition)

This way, the workspace gets these arguments. But the workspace does not yet know
these arguments. We fix that in the file 'farg/apps/numeric_bongard/workspace.py'.
The constructor currently looks like this::

  def __init__(self):
    pass

For now, we will just make it recognize the new values without doing anything
useful with it::

  def __init__(self, *, left_integers, right_integers):
    pass

