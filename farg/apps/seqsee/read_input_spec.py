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

from farg.core.read_input_spec import ReadInputSpec, SpecificationForOneRun

class SeqseeReadInputSpec(ReadInputSpec):
  def ReadLine(self, line):
    if not '|' in line:
      return
    input, continuation = (x.split() for x in line.strip().split('|'))
    yield SpecificationForOneRun(' '.join(input),
                                 dict(sequence=' '.join(input),
                                      unrevealed_terms=' '.join(continuation)))
