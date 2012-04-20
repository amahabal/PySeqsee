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

class Binding(object):
  """Specification of how an instance is a member of some category.
  
  .. Note::
  
    In the Perl version, the bindings had special slots for squinting, position, metotype
    etc. Here, all are part of the same hash, along with "regular" attributes such as length.
  
    This also means that the caller of the constructor needs to do all the work, unlike in
    Perl, where some bits were calculated by the constructor. 
  """
  def __init__(self, **bindings):
    self.bindings = dict(bindings)

  def GetBindingsForAttribute(self, attribute_name):
    """Get the binding of a single attribute."""
    return self.bindings[attribute_name]

  def __str__(self):
    return 'Bindings: %s' % self.bindings
