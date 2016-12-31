How to add flags to the application
====================================

From the GFlags Documentation:
"This module is used to define and parse command line flags.

This module defines a *distributed* flag-definition policy: rather than
an application having to define all flags in or near main(), each python
module defines flags that are useful to it.  When one python module
imports another, it gains access to the other's flags.  (This is
implemented by having all modules share a common, global registry object
containing all the flag information.)

Flags are defined through the use of one of the DEFINE_xxx functions.
The specific function used determines how the flag is parsed, checked,
and optionally type-converted, when it's seen on the command line.


IMPLEMENTATION: DEFINE_* creates a 'Flag' object and registers it with a
'FlagValues' object (typically the global FlagValues FLAGS, defined
here).  The 'FlagValues' object can scan the command line arguments and
pass flag arguments to the corresponding 'Flag' objects for
value-checking and type conversion.  The converted flag values are
available as attributes of the 'FlagValues' object.

Code can access the flag through a FlagValues object, for instance
gflags.FLAGS.myflag.  Typically, the __main__ module passes the command
line arguments to gflags.FLAGS for parsing.

At bottom, this module calls getopt(), so getopt functionality is
supported, including short- and long-style flags, and the use of -- to
terminate flags.

Methods defined by the flag module will throw 'FlagsError' exceptions.
The exception argument will be a human-readable string.


FLAG TYPES: This is a list of the DEFINE_*'s that you can do.  All flags
take a name, default value, help-string, and optional 'short' name
(one-letter name).  Some flags have other arguments, which are described
with the flag.

DEFINE_string: takes any input, and interprets it as a string.

DEFINE_bool or
DEFINE_boolean: typically does not take an argument: say --myflag to
                set FLAGS.myflag to true, or --nomyflag to set
                FLAGS.myflag to false.  Alternately, you can say
                   --myflag=true  or --myflag=t or --myflag=1  or
                   --myflag=false or --myflag=f or --myflag=0

DEFINE_float: takes an input and interprets it as a floating point
              number.  Takes optional args lower_bound and upper_bound;
              if the number specified on the command line is out of
              range, it will raise a FlagError.

DEFINE_integer: takes an input and interprets it as an integer.  Takes
                optional args lower_bound and upper_bound as for floats.

DEFINE_enum: takes a list of strings which represents legal values.  If
             the command-line value is not in this list, raise a flag
             error.  Otherwise, assign to FLAGS.flag as a string.

DEFINE_list: Takes a comma-separated list of strings on the commandline.
             Stores them in a python list object.

DEFINE_spaceseplist: Takes a space-separated list of strings on the
                     commandline.  Stores them in a python list object.
                     Example: --myspacesepflag "foo bar baz"

DEFINE_multistring: The same as DEFINE_string, except the flag can be
                    specified more than once on the commandline.  The
                    result is a python list object (list of strings),
                    even if the flag is only on the command line once.

DEFINE_multi_int: The same as DEFINE_integer, except the flag can be
                  specified more than once on the commandline.  The
                  result is a python list object (list of ints), even if
                  the flag is only on the command line once.


SPECIAL FLAGS: There are a few flags that have special meaning:
   --help          prints a list of all the flags in a human-readable fashion
   --helpshort     prints a list of all key flags (see below).
   --helpxml       prints a list of all flags, in XML format.  DO NOT parse
                   the output of --help and --helpshort.  Instead, parse
                   the output of --helpxml.  For more info, see
                   "OUTPUT FOR --helpxml" below.
   --flagfile=foo  read flags from file foo.
   --undefok=f1,f2 ignore unrecognized option errors for f1,f2.
                   For boolean flags, you should use --undefok=boolflag, and
                   --boolflag and --noboolflag will be accepted.  Do not use
                   --undefok=noboolflag.
   --              as in getopt(), terminates flag-processing


FLAGS VALIDATORS: If your program:
  - requires flag X to be specified
  - needs flag Y to match a regular expression
  - or requires any more general constraint to be satisfied
then validators are for you!

Each validator represents a constraint over one flag, which is enforced
starting from the initial parsing of the flags and until the program
terminates.

Also, lower_bound and upper_bound for numerical flags are enforced using flag
validators.

Howto:
If you want to enforce a constraint over one flag, use

gflags.RegisterValidator(flag_name,
                        checker,
                        message='Flag validation failed',
                        flag_values=FLAGS)

After flag values are initially parsed, and after any change to the specified
flag, method checker(flag_value) will be executed. If constraint is not
satisfied, an IllegalFlagValue exception will be raised. See
RegisterValidator's docstring for a detailed explanation on how to construct
your own checker.


EXAMPLE USAGE:

FLAGS = gflags.FLAGS

gflags.DEFINE_integer('my_version', 0, 'Version number.')
gflags.DEFINE_string('filename', None, 'Input file name', short_name='f')

gflags.RegisterValidator('my_version',
                        lambda value: value % 2 == 0,
                        message='--my_version must be divisible by 2')
gflags.MarkFlagAsRequired('filename')


NOTE ON --flagfile:

Flags may be loaded from text files in addition to being specified on
the commandline.

Any flags you don't feel like typing, throw them in a file, one flag per
line, for instance:
   --myflag=myvalue
   --nomyboolean_flag
You then specify your file with the special flag '--flagfile=somefile'.
You CAN recursively nest flagfile= tokens OR use multiple files on the
command line.  Lines beginning with a single hash '#' or a double slash
'//' are comments in your flagfile.

Any flagfile=<file> will be interpreted as having a relative path from
the current working directory rather than from the place the file was
included from:
   myPythonScript.py --flagfile=config/somefile.cfg

If somefile.cfg includes further --flagfile= directives, these will be
referenced relative to the original CWD, not from the directory the
including flagfile was found in!

The caveat applies to people who are including a series of nested files
in a different dir than they are executing out of.  Relative path names
are always from CWD, not from the directory of the parent include
flagfile. We do now support '~' expanded directory names.

Absolute path names ALWAYS work!


EXAMPLE USAGE:


  FLAGS = gflags.FLAGS

  # Flag names are globally defined!  So in general, we need to be
  # careful to pick names that are unlikely to be used by other libraries.
  # If there is a conflict, we'll get an error at import time.
  gflags.DEFINE_string('name', 'Mr. President', 'your name')
  gflags.DEFINE_integer('age', None, 'your age in years', lower_bound=0)
  gflags.DEFINE_boolean('debug', False, 'produces debugging output')
  gflags.DEFINE_enum('gender', 'male', ['male', 'female'], 'your gender')

  def main(argv):
    try:
      argv = FLAGS(argv)  # parse flags
    except gflags.FlagsError, e:
      print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], FLAGS)
      sys.exit(1)
    if FLAGS.debug: print 'non-flag arguments:', argv
    print 'Happy Birthday', FLAGS.name
    if FLAGS.age is not None:
      print 'You are a %d year old %s' % (FLAGS.age, FLAGS.gender)

  if __name__ == '__main__':
    main(sys.argv)


KEY FLAGS:

As we already explained, each module gains access to all flags defined
by all the other modules it transitively imports.  In the case of
non-trivial scripts, this means a lot of flags ...  For documentation
purposes, it is good to identify the flags that are key (i.e., really
important) to a module.  Clearly, the concept of "key flag" is a
subjective one.  When trying to determine whether a flag is key to a
module or not, assume that you are trying to explain your module to a
potential user: which flags would you really like to mention first?

We'll describe shortly how to declare which flags are key to a module.
For the moment, assume we know the set of key flags for each module.
Then, if you use the app.py module, you can use the --helpshort flag to
print only the help for the flags that are key to the main module, in a
human-readable format.

NOTE: If you need to parse the flag help, do NOT use the output of
--help / --helpshort.  That output is meant for human consumption, and
may be changed in the future.  Instead, use --helpxml; flags that are
key for the main module are marked there with a <key>yes</key> element.

The set of key flags for a module M is composed of:

1. Flags defined by module M by calling a DEFINE_* function.

2. Flags that module M explictly declares as key by using the function

     DECLARE_key_flag(<flag_name>)

3. Key flags of other modules that M specifies by using the function

     ADOPT_module_key_flags(<other_module>)

   This is a "bulk" declaration of key flags: each flag that is key for
   <other_module> becomes key for the current module too.

Notice that if you do not use the functions described at points 2 and 3
above, then --helpshort prints information only about the flags defined
by the main module of our script.  In many cases, this behavior is good
enough.  But if you move part of the main module code (together with the
related flags) into a different module, then it is nice to use
DECLARE_key_flag / ADOPT_module_key_flags and make sure --helpshort
lists all relevant flags (otherwise, your code refactoring may confuse
your users).

Note: each of DECLARE_key_flag / ADOPT_module_key_flags has its own
pluses and minuses: DECLARE_key_flag is more targeted and may lead a
more focused --helpshort documentation.  ADOPT_module_key_flags is good
for cases when an entire module is considered key to the current script.
Also, it does not require updates to client scripts when a new flag is
added to the module.


EXAMPLE USAGE 2 (WITH KEY FLAGS):

Consider an application that contains the following three files (two
auxiliary modules and a main module)

File libfoo.py:

  import gflags

  gflags.DEFINE_integer('num_replicas', 3, 'Number of replicas to start')
  gflags.DEFINE_boolean('rpc2', True, 'Turn on the usage of RPC2.')

  ... some code ...

File libbar.py:

  import gflags

  gflags.DEFINE_string('bar_gfs_path', '/gfs/path',
                      'Path to the GFS files for libbar.')
  gflags.DEFINE_string('email_for_bar_errors', 'bar-team@google.com',
                      'Email address for bug reports about module libbar.')
  gflags.DEFINE_boolean('bar_risky_hack', False,
                       'Turn on an experimental and buggy optimization.')

  ... some code ...

File myscript.py:

  import gflags
  import libfoo
  import libbar

  gflags.DEFINE_integer('num_iterations', 0, 'Number of iterations.')

  # Declare that all flags that are key for libfoo are
  # key for this module too.
  gflags.ADOPT_module_key_flags(libfoo)

  # Declare that the flag --bar_gfs_path (defined in libbar) is key
  # for this module.
  gflags.DECLARE_key_flag('bar_gfs_path')

  ... some code ...

When myscript is invoked with the flag --helpshort, the resulted help
message lists information about all the key flags for myscript:
--num_iterations, --num_replicas, --rpc2, and --bar_gfs_path.

Of course, myscript uses all the flags declared by it (in this case,
just --num_replicas) or by any of the modules it transitively imports
(e.g., the modules libfoo, libbar).  E.g., it can access the value of
FLAGS.bar_risky_hack, even if --bar_risky_hack is not declared as a key
flag for myscript.


OUTPUT FOR --helpxml:

The --helpxml flag generates output with the following structure:

<?xml version="1.0"?>
<AllFlags>
  <program>PROGRAM_BASENAME</program>
  <usage>MAIN_MODULE_DOCSTRING</usage>
  (<flag>
    [<key>yes</key>]
    <file>DECLARING_MODULE</file>
    <name>FLAG_NAME</name>
    <meaning>FLAG_HELP_MESSAGE</meaning>
    <default>DEFAULT_FLAG_VALUE</default>
    <current>CURRENT_FLAG_VALUE</current>
    <type>FLAG_TYPE</type>
    [OPTIONAL_ELEMENTS]
  </flag>)*
</AllFlags>

Notes:

1. The output is intentionally similar to the output generated by the
C++ command-line flag library.  The few differences are due to the
Python flags that do not have a C++ equivalent (at least not yet),
e.g., DEFINE_list.

2. New XML elements may be added in the future.

3. DEFAULT_FLAG_VALUE is in serialized form, i.e., the string you can
pass for this flag on the command-line.  E.g., for a flag defined
using DEFINE_list, this field may be foo,bar, not ['foo', 'bar'].

4. CURRENT_FLAG_VALUE is produced using str().  This means that the
string 'false' will be represented in the same way as the boolean
False.  Using repr() would have removed this ambiguity and simplified
parsing, but would have broken the compatibility with the C++
command-line flags.

5. OPTIONAL_ELEMENTS describe elements relevant for certain kinds of
flags: lower_bound, upper_bound (for flags that specify bounds),
enum_value (for enum flags), list_separator (for flags that consist of
a list of values, separated by a special token).

6. We do not provide any example here: please use --helpxml instead.

This module requires at least python 2.2.1 to run."
