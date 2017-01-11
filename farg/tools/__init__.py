from farg.tools import create_app
import os.path
import sys, os, shutil, runpy

def main():
  """
  Main function that looks at the given args and runs the correct function
  """
  try:
    command = sys.argv[1]
    if command == "create":
      create(sys.argv[2])
    elif command == "run":
      try:
        args = " ".join(sys.argv[3:])
      except Exception:
        args = ""
      run(sys.argv[2], args)
    elif command == "remove":
      remove(sys.argv[2])
    elif command == "help":
      print('Usage: "farg <command> <command arguments>"')
      print('\tCommands:')
      print('\tfarg create foo \t creates an app called foo')
      print('\tfarg run foo <args> \t runs the app foo, with optional arguments')
      print('\tfarg remove foo \t removes the app foo')
  except Exception:
    print('Command not recognized.  Run farg help to see availiable commands.')
    sys.exit(1)
      
    
    
def create(appName):
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
  create_app.FARGApp().run(appName, install_prefix=install_prefix)

def run (appName, args):
  try:
    print('Executing python3 -m farg.apps.{0}.run_{1} {2}'.format(appName, appName, args))
    os.system('python3 -m farg.apps.{0}.run_{1} {2}'.format(appName, appName, args))
  except ImportError as e:
    print ('Error: app "{0}" not found'.format(appName))
    print (e)

def remove(appName):
  yOrN = input("Are you sure you want to remove {}? This cannot be undone. [y/n] ".format(appName))

  if yOrN[0].lower() == "y":
    dirToRemove = os.path.join(os.getcwd(), 'farg', 'apps', appName.lower())
    print ("Removing " + dirToRemove + "...")
    shutil.rmtree(dirToRemove)
  else:
    print ("Cancelling...")
