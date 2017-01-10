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

"""Utility functions for Seqsee.

These include:

* Comparator functions *LessThan*, *LessThanEq*, *GreaterThan*, *GreaterThanEq*, *Exactly*, each of
  which takes a single argument and returns a one-argument function.
"""

def LessThan(x):
  def fn(y): return y < x
  return fn

def LessThanEq(x):
  def fn(y): return y <= x
  return fn

def GreaterThan(x):
  def fn(y): return y > x
  return fn

def GreaterThanEq(x):
  def fn(y): return y >= x
  return fn

def Exactly(x):
  def fn(y): return y == x
  return fn
