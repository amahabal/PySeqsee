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

def WeightedChoice(choices):
  """Choices is an iterable of 2-tuples, where the second value is the weight. Chooses one."""
  total = sum(w for c, w in choices)
  r = random.uniform(0, total)
  upto = 0
  for c, w in choices:
    if upto + w > r:
      return c
    upto += w
  assert False, "Shouldn't get here"

def WeightedShuffle(choices):
  """Choices is an iterable of 2-tuples, where the second value is the weight.
  
  Returns a shuffle of the first elements based on the weight."""
  total = sum(w for c, w in choices)
  while total > 0:
    r = random.uniform(0, total)
    upto = 0
    for idx, ch in enumerate(choices):
      c, w = ch
      if upto + w > r:
        total -= w
        choices = choices[0:idx] + choices[idx + 1:]
        yield c
        continue
      upto += w
