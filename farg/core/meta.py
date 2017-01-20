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
from farg.core.exceptions import FargError
"""Metaclass that makes the constructor memoized.

That is, if the constructor is called twice with identical arguments, the same instance is
returned in both cases.
"""

from abc import ABCMeta

class MemoizedConstructor(ABCMeta):
  """Metaclass that makes the constructor memoized.

  That is, if the constructor is called twice with identical arguments, the same instance is
  returned in both cases.

  .. Note::

    The memoization fails when the constructor is sometimes called with positional arguments, and
    at other times with the equivalent keyword arguments. If the classes using this as a metaclass
    only support KW args, this is a non-issue.
  """

  def __init__(mcs, name, bases, class_dict):
    """Called when a class with this metaclass is defined."""
    super(MemoizedConstructor, mcs).__init__(name, bases, class_dict)
    mcs.__memo__ = dict()

  def __call__(mcs, *args, **kw):
    """Called when the constructor of that class is called."""
    # This barfs when constructor of the child class is called with a positional argument. I wonder
    # if I can do this earlier (at class construction time)?
    if args:
      raise FargError("Child classes of MemoizedConstructor should not have postional args")
    memo_key = (tuple(args), frozenset(list(kw.items())))
    if memo_key not in mcs.__memo__:
      mcs.__memo__[memo_key] = super(MemoizedConstructor, mcs).__call__(*args, **kw)
    return mcs.__memo__[memo_key]
