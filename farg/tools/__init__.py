from farg.tools import create_app
import os.path
import sys, os, shutil

def main():
  """
  Main function that looks at the given args and runs the correct function
  """
  command = sys.argv[1]
  
  if len(sys.argv) != 3:
      print('Expected exactly two arguments of the form <command> <name of app>. Got %d instead (%s)' %
        (len(sys.argv) - 1, sys.argv[1:]))
      sys.exit(1)
      
  if command == "create":
    create(sys.argv[2])
  elif command == "remove":
    remove(sys.argv[2])
      
    
    
def create(name):
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
    
  create_app.FARGApp().run(name, install_prefix=install_prefix)
  
def remove(name):
  yOrN = input("Are you sure you want to remove {}? This cannot be undone. [y/n] ".format(name))
  

  if yOrN[0].lower() == "y":
    dirToRemove = os.path.join(os.getcwd(), 'farg', 'apps', name.lower())
    print ("Removing " + dirToRemove + "...")
    shutil.rmtree(dirToRemove)
  else:
    print ("Cancelling...")
