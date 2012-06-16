# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>
"""Basic Input specification reader.

When running batch or sxs, the application should be run on several different inputs (usually
with expected outputs specified). The class in this module can be used directly or extended
to parse such a file.
"""


class SpecificationForOneRun:
  """Specification of input flags for a single run."""

  def __init__(self, name, arguments_dict):
    #: Name of the input, for display purposes.
    self.name = name
    #: The dictionary of arguments to be passed to the application for that input. Typically,
    #: this will contain two keys: 'input' and 'expected output', but could be anything,
    #: depending on the application.
    self.arguments_dict = arguments_dict


class ReadInputSpec:
  """Basic Input specification reader.

  Features of this reader:

    * One input per line.
    * Empty lines and those starting with # are ignored.
    * Lines are split on the first '|', and the left part becomes the input, the right is the
      expected output.

  This can be subclassed to read a different type of file.
  """

  def __init__(self):
    pass

  def ReadFile(self, filename):
    """Reads in specification from a file."""
    return self.ReadLines(open(filename))

  def ReadLines(self, filelike):
    """Reads specification from string iterator."""
    for line in filelike:
      if not line.strip():
        continue
      if line.strip().startswith('#'):
        continue
      for spec in self.ReadLine(line):
        yield spec

  def ReadLine(self, line):  # Should be a method so can be overridden. pylint:disable=R0201
    """Read a single non-empty non-comment line, converting it to a Specification."""
    if not '|' in line:
      return
    input_string, expected_output = (x.strip() for x in line.strip().split('|'))
    yield SpecificationForOneRun(input_string,
                                 dict(input=input_string,
                                      expected_output=expected_output))
