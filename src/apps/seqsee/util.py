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
