"""Utility functions for Seqsee.

These include:

* Comparator functions *LessThan*, *LessThanEq*, *GreaterThan*, *GreaterThanEq*, *Exactly*, each of
  which takes a single argument and returns a one-argument function.
* Toss(x), which returns True with probability x.
"""

import random

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

def Toss(x):
  """x is a number between 0 and 1. Returns true with probability x."""
  return random.uniform(0, 1) <= x
