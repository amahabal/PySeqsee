from farg.tools import create_app
import os.path
import sys, os, shutil, runpy

def main():
  """
  Main function that looks at the given args and runs the correct function
  """
  try:
    command = sys.argv[1]
    if command == "update":
      update()
    if command == "create":
      create(sys.argv[2])
    elif command == "run":
      try:
        args = " ".join(sys.argv[3:])
      except Exception:
        args = ""
      run(sys.argv[2], args)
    elif command == "codelet":
      appName = sys.argv[2]
      codeletName = sys.argv[3]
      addCodelet(appName, codeletName)
    elif command == "test":
      if len(sys.argv) == 2: #That'd be `farg test`
        os.system("nosetests --pdb ./tests/")
      else: #Hopefully the user is in the root directory of PySeqsee
        if sys.argv[2] == "core":
          os.system("nosetests --pdb farg/core/tests/".format(sys.argv[2]))
        else:
          os.system("nosetests --pdb farg/apps/{0}/tests/".format(sys.argv[2]))
      sys.exit(0)
    elif command == "remove":
      remove(sys.argv[2])
    elif command == "help":
      print ('Usage: "farg <command> <command arguments>"')
      print ('\tCommands:')
      print ('\tfarg create foo \t creates an app called foo')
      print ('\tfarg run foo <args> \t runs the app foo, with optional arguments')
      print ('\tfarg codelet foo bar \t adds a codelet named bar to the app foo')
      print ('\tfarg test [foo (optional)] \t runs nosetests on the app in the current directory, or app foo, if in root directory')
      print ('\tfarg remove foo \t removes the app foo')
      print ('\tfarg update \t updates farg to the latest version using git.  This should be done periodically as PySeqsee is in active development.')
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

def addCodelet (appName, codeletName):
  codeletPath = os.path.join(os.getcwd(), 'farg', 'apps', appName.lower(), 'codelet_families', 'all.py')
  codeletFile = open(codeletPath, "a+")
  template = ("\nclass CF_{0}(CodeletFamily):\n"
              "   '''One line documentation of what codelets of this family do.\n"          
              "    Documentation describes what it does, what codelets it may create, what things\n"
              "    it may cause to focus on, and any subspace it may be a part of.\n"
              "    '''\n"
              "\n"
              "    @classmethod\n"
              "    def Run(cls, controller, *):\n"
              "      '''One line documentation of what codelets of this family do.\n"
              "\n"
              "      Run may take extra arguments (such as other_arg1 above). The extra arguments\n"
              "      will be passed by name only. These are set in the constructor of the codelet.\n"
              "      '''\n"
              "      #TODO: Write out what this codelet does\n").format(codeletName)
  codeletFile.write(template)
  print ("Now edit " + codeletPath + " to describe what the codelet does.")
  
def remove(appName):
  yOrN = input("Are you sure you want to remove {}? This cannot be undone. [y/n] ".format(appName))
  dirToRemove = os.path.join(os.getcwd(), 'farg', 'apps', appName.lower().replace(" ", ""))
  if yOrN[0].lower() == "y":
    dirToRemove = os.path.join(os.getcwd(), 'farg', 'apps', appName.lower())
    print ("Removing " + dirToRemove + "...")
    shutil.rmtree(dirToRemove)
  else:
    print ("Cancelling...")
    
def update():
  os.system("git pull")
  returnCode = os.system("python3 setup.py install")
  if returnCode != 0:
    print ("Install failed, retrying using 'sudo'")
    os.system("sudo python3 setup.py install")
  
if __name__ == "__main__":
  main()
