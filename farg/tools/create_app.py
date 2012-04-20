"""
Script to create an empty application.
"""
from argparse import ArgumentError
from farg.third_party.skeleton import Skeleton, Var
from farg.third_party.skeleton.core import ValidateError
import os.path
import sys

class VarWithConstraints(Var):
  def __init__(self, name, *, constraint, **kwargs):
    Var.__init__(self, name, **kwargs)
    self.constraint = constraint

  def validate(self, response):
    validated_value = Var.validate(self, response)
    if not self.constraint(validated_value):
      raise ValidateError('Response "%s" did not match constraint.' % response)
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
  if os.path.exists(src):
    print("Using templates in ", src)
  else:
    print("Unable to locate templates in ", src)
    src = os.path.join(sys.prefix, 'data', 'pyseqsee_app_template')
    if os.path.exists(src):
      print("Using templates in ", src)
    else:
      print("Unable to locate templates in ", src)
      print("Giving up. You should be in the root of the PySeqsee distribution, or have "
            "PySeqsee installed. (Currently, only the first of these works for this script).")
  variables = []

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
    self.variables.append(VarWithConstraints('application_class',
                                             description='capitalized version of %s' % dst_dir,
                                             constraint=(lambda x: dst_dir == x.lower()),
                                             default=dst_dir[0].upper() + dst_dir[1:]))
    Skeleton.run(self, new_dst_dir, run_dry)


def main():
  """Basic command line bootstrap for the BasicModule Skeleton"""
  # Check that there is an apps subdirectory.
  if not(os.path.exists('farg')) or not (os.path.isdir('farg')):
    raise Exception('Should be called from a directory containing farg')
  subdir = os.path.join('farg', 'apps')
  if not(os.path.exists(subdir)) or not (os.path.isdir(subdir)):
    raise Exception('Should be called from a directory containing %s' % subdir)

  if len(sys.argv) != 2:
    raise Exception('Expected exactly one argument (name of app to create)')

  FARGApp().run(sys.argv[1])

if __name__ == '__main__':
  main()
