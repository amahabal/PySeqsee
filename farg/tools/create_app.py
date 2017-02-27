"""
Script to create an empty application.
"""
from argparse import ArgumentError
import os.path
import sys

from farg.third_party.skeleton import Skeleton, Var
from farg.third_party.skeleton.core import ValidateError
class VarWithConstraints(Var):
  def __init__(self, name, *, constraint, **kwargs):
    Var.__init__(self, name, **kwargs)
    self.constraint = constraint

  def validate(self, response):
    validated_value = Var.validate(self, response)
    if not self.constraint(validated_value):
      constraints = ("\n=====Constraints:\nFor application name: should be lowercase.\n"
                     "For class name: its lowercase version should match the app name, not "
                     "counting underscores (that is, they can be 'foo' and 'F_O_o')")
      raise ValidateError('Response "%s" did not match constraint. %s' % (response,
                                                                          constraints))
    return validated_value

def ApplicationNameConstraint(app_name):
  if app_name != app_name.lower():
    return False
  return True

class FARGApp(Skeleton):
  """
  Create an empty FARG application.
  """
  src = os.path.join(os.path.realpath(os.path.curdir), 'data', 'pyseqsee_app_template')
  if not os.path.exists(src):
    print("Unable to locate templates in ", src)
    src = os.path.join(sys.prefix, 'data', 'pyseqsee_app_template')
    if os.path.exists(src):
      print("Using templates in ", src)
    else:
      print("Unable to locate templates in ", src)
      print("Giving up. You should be in the root of the PySeqsee distribution, or have "
            "PySeqsee installed. (Currently, only the first of these works for this script).")
  variables = []

  def CapitalizeName(self, application_name):
    """Convert application_name to uppercase.

       underscores are dropped, and letters after underscores are uppercases.
    """
    return ''.join(x[0].upper() + x[1:] for x in application_name.split('_'))

  def AreNamesConsistent(self, dst_dir, class_name):
    return dst_dir.lower().replace('_', '') == class_name.lower().replace('_', '')

  def run(self, dst_dir, run_dry=False, install_prefix=''):
    """
    Override run to use a different dst_dir: apps/dst_dir, and to bail out if it exists.
    Furthermore, it bails out if the dst_dir is not the same as the app name.
    """
    if not ApplicationNameConstraint(dst_dir):
      raise Exception('Application name should be lowercase. "%s" is not.' % dst_dir)
    new_dst_dir = os.path.join(install_prefix, dst_dir)
    print('New Destination: ', new_dst_dir)
    if os.path.exists(new_dst_dir):
      raise Exception("Directory already exists (%s). Won't overwrite." % new_dst_dir)
    self.variables.append(VarWithConstraints('application_name',
                                             description='should be lowercase',
                                             constraint=ApplicationNameConstraint,
                                             default=dst_dir))
    self.set_variables['application_name'] = dst_dir
    self.variables.append(VarWithConstraints(
        'application_class',
        description='capitalized version of "%s"' % dst_dir,
        constraint=lambda x: self.AreNamesConsistent(x, dst_dir),
        default=self.CapitalizeName(dst_dir)))
    Skeleton.run(self, new_dst_dir, run_dry)
    print("\n==============================================\n",
          "\nYou may now run the app (which as yet does nothing) like so:\n\n",
          "farg run %s\n\n" % dst_dir,
          "What next? That documentation is currently sketchy, but is being updated.")

if __name__ == '__main__':
  print("\n============= ERROR ==============")
  print("This file should no longer be executed directly. Instead, use "
        "'farg create' in this directory.")
