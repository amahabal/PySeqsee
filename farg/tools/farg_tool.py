from farg.tools import create_app
import os.path
import sys, os, shutil, runpy
import argparse

def create(args):
  """Basic command line bootstrap for the BasicModule Skeleton"""
  appName = args.app_name
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

def run_app(args):
  appName = args.app_name
  rest = " ".join(args.rest)
  try:
    print('Executing python3 -m farg.apps.{0}.run_{1} {2}'.format(appName, appName, rest))
    os.system('python3 -m farg.apps.{0}.run_{1} {2}'.format(appName, appName, rest))
  except ImportError as e:
    print ('Error: app "{0}" not found'.format(appName))
    print (e)

def addCodelet (args):
  appName = args.app_name
  codeletName = args.codelet_name
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
  
def remove(args):
  appName = args.app_name
  yOrN = input("Are you sure you want to remove {}? This cannot be undone. [y/n] ".format(appName))
  dirToRemove = os.path.join(os.getcwd(), 'farg', 'apps', appName.lower().replace(" ", ""))
  if yOrN[0].lower() == "y":
    dirToRemove = os.path.join(os.getcwd(), 'farg', 'apps', appName.lower())
    print ("Removing " + dirToRemove + "...")
    shutil.rmtree(dirToRemove)
  else:
    print ("Cancelling...")
    
def update(args):
  os.system("git pull")
  returnCode = os.system("python3 setup.py install")
  if returnCode != 0:
    print ("Install failed, retrying using 'sudo'")
    os.system("sudo python3 setup.py install")

def run_tests(args):
  if args.app_name == "core":
    os.system("nosetests --pdb farg/core/tests/")
  else:
    os.system("nosetests --pdb farg/apps/{0}/tests/".format(args.app_name))

def main():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers(help="For detailed help, try --help after command (e.g., run --help)")

  parser_run = subparsers.add_parser('run', help='Run an app. For detailed help, add --help after app name (e.g., run seqsee --help)')
  parser_run.add_argument('app_name', help='Name of app to create (all lowercase)')
  parser_run.add_argument('rest', nargs=argparse.REMAINDER, help='Remaining arguments to pass on to app')
  parser_run.set_defaults(func=run_app)

  parser_create = subparsers.add_parser('create', help='Create skeleton for a new app')
  parser_create.add_argument('app_name', help='Name of app to create (all lowercase)')
  parser_create.set_defaults(func=create)

  parser_create_codelet = subparsers.add_parser('codelet', help='Add a codelet family')
  parser_create_codelet.add_argument('app_name', help='Name of app to create (all lowercase)')
  parser_create_codelet.add_argument('codelet_name', help='Codelet family to create (without CF_prefix)')
  parser_create_codelet.set_defaults(func=addCodelet)

  parser_remove = subparsers.add_parser('remove', help='remove existing app')
  parser_remove.add_argument('app_name', help='Name of app to remove (all lowercase)')
  parser_remove.set_defaults(func=remove)

  parser_test = subparsers.add_parser('test', help='Run tests')
  parser_test.add_argument('app_name', help='Name of app to test. Use "core" for core tests')
  parser_test.set_defaults(func=run_tests)

  parser_update = subparsers.add_parser('update', help='Updates farg to latest version using git')
  parser_update.set_defaults(func=update)

  args = parser.parse_args()
  if not hasattr(args, 'func'):
    parser.print_help()
    sys.exit()
  args.func(args)


if __name__ == "__main__":
  main()
