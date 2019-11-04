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
"""Specification of how an instance is a member of some category."""


class Binding:
    """Specification of how an instance is a member of some category."""

    def __init__(self, **bindings):
        self.bindings = dict(bindings)

    def GetBindingsForAttribute(self, attribute_name):
        """Get the binding of a single attribute."""
        return self.bindings[attribute_name]

    def __str__(self):
        serialided_dict = dict((k, str(v)) for k, v in self.bindings.items())
        return 'Bindings: %s' % serialided_dict
