#!/usr/bin/python3
"""
Script to create an empty application.
"""
from farg.tools import create_app
import os.path
import sys

def main():
  """Basic command line bootstrap for the BasicModule Skeleton"""
  # Check that there is an apps subdirectory.
  subdir = os.path.join('farg', 'apps')
  if (os.path.exists('farg') and os.path.isdir('farg') and
      os.path.exists(subdir) and os.path.isdir(subdir)):
    install_prefix = subdir
  else:
    install_prefix = ''
    print('!!!!!!!!!!!!!!!!!!!!!!!', "\n",
          'Creating an app in a directory other than the root of PySeqsee is not yet '
          'supported.\nIf you need this soon, email pyseqsee@googlegroups.com and it will '
          'be prioritized.', "\n", '!!!!!!!!!!!!!!!!!!!!!!!', "\n")
    sys.exit(1)

  if len(sys.argv) != 2:
    print('Expected exactly one argument (the name of the script). Got %d instead (%s)' %
          (len(sys.argv) - 1, sys.argv[1:]))
    sys.exit(1)

  create_app.FARGApp().run(sys.argv[1], install_prefix=install_prefix)

if __name__ == '__main__':
  main()
