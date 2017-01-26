from farg.core.codelet import CodeletFamily

class CF_HorribleHack(CodeletFamily):
  '''Checks if the solution is odd/even.

     This is here merely for demonstration purposes. See :doc:`new_app/first_codelet` for details.
  '''
  @classmethod
  def Run(cls, controller, *, me):
    '''Check if solution is even/odd.'''
    workspace = controller.workspace
    if (all(x.magnitude % 2 == 1 for x in workspace.left_items) and
        all(x.magnitude % 2 == 0 for x in workspace.right_items)):
      controller.ui.DisplayMessage("This is an odd/even split")
    else:
      controller.ui.DisplayMessage("I have no idea what this sequence is")
