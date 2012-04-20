from distutils.core import setup
import os
import sys

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
farg_dir = 'farg'
for dirpath, dirnames, filenames in os.walk(farg_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
      # print('In %s, saw Dir: %s' % (dirpath, dirname))
      if dirname.startswith('.') or dirname == '__pycache__':
        del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
for dirpath, dirnames, filenames in os.walk('data/pyseqsee_app_template'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.') or dirname == '__pycache__':
          del dirnames[i]
    if filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])
# Small hack for working with bdist_wininst.
# See http://mail.python.org/pipermail/distutils-sig/2004-August/004134.html
if len(sys.argv) > 1 and sys.argv[1] == 'bdist_wininst':
    for file_info in data_files:
        file_info[0] = '\\PURELIB\\%s' % file_info[0]

# Dynamically calculate the version based on django.VERSION.
version = __import__('farg').get_version()
setup(
    name="PySeqsee",
    version=version,
    url='https://github.com/amahabal/PySeqsee',
    author='Abhijit Mahabal',
    author_email='pyseqsee@googlegroups.com',
    description="Python framework for writing programs to solve complex problems not amenable to brute force. The architecture is a descendant of Douglas Hofstadter and Melanie Mitchell's Copycat architecture.",
    packages=packages,
    data_files=data_files,
    scripts=['farg/tools/pyseqsee_create_app.py'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.1',
   ],
)
