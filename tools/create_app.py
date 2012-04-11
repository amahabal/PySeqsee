"""
Script to create an empty application.
"""
import os.path
from skeleton import Skeleton, Var
from skeleton.core import ValidateError
from argparse import ArgumentError

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
  src = 'application_template'
  variables = []

  def run(self, dst_dir, run_dry=False):
    """
    Override run to use a different dst_dir: apps/dst_dir, and to bail out if it exists.
    Furthermore, it bails out if the dst_dir is not the same as the app name.
    """
    if not ApplicationNameConstraint(dst_dir):
      raise Exception('Application name should be lowercase. "%s" is not.' % dst_dir)
    new_dst_dir = 'apps/%s' % dst_dir
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
  if not(os.path.exists('apps')) or not (os.path.isdir('apps')):
    raise Exception('Should be called from a directory containing apps')
  FARGApp.cmd()

if __name__ == '__main__':
  main()
