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

class MemoizedConstructor(type):
  def __init__(self, name, bases, class_dict):
    super(MemoizedConstructor, self).__init__(name, bases, class_dict)
    self.__memo__ = dict()

  def __call__(self, *args, **kw):
    memo_key = (tuple(args), frozenset(list(kw.items())))
    if memo_key not in self.__memo__:
      self.__memo__[memo_key] = super(MemoizedConstructor, self).__call__(*args, **kw)
    return self.__memo__[memo_key]
