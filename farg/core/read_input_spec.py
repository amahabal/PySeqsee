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

class SpecificationForOneRun:
  """Specification of input flags for a single run"""
  def __init__(self, name, arguments_dict):
    self.name = name
    self.arguments_dict = arguments_dict

class ReadInputSpec:
  """Class to read in examples to test the program on."""

  def ReadFile(self, filename):
    """Reads in specification from a file."""
    return self.ReadLines(open(filename))

  def ReadLines(self, filelike):
    """Reads specification from string iterator."""
    for line in filelike:
      if line.strip().startswith('#'):
        continue
      for spec in self.ReadLine(line):
        yield spec

  def ReadLine(self, line):
    if not '|' in line:
      return
    input, expected_output = (x.strip() for x in line.strip().split('|'))
    yield SpecificationForOneRun(input,
                                 dict(input=input,
                                      expected_output=expected_output))
