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

import colorsys
import random

def HSVToColorString(hue, saturation, value):
  """Convert from HSV to RGB color space."""
  rgb = ('%02x' % (255.0 * x) for x in colorsys.hsv_to_rgb(hue, saturation, value))
  return '#' + ''.join(rgb)

def Toss(x):
  """x is a number between 0 and 1. Returns true with probability x."""
  return random.uniform(0, 1) <= x

def ChooseAboutN(n, choices):
  """Choose in a way that the expected number of choices is n.
  
  Choices is an iterable of 2-tuples, where the second value is the weight.
  
  An example to show how it works: let choices contain 5 things with weights 10, 20, 30
  40, and 50 (thus summing to 150), and let n=3. Then we will keep the first item in the
  output with probability 3 * 10/150 (i.e., 20%).
  """
  choices = list(choices)  # Needed since we iterate twice over the iterable.
  total = sum(w for _c, w in choices)
  return [x[0] for x in choices if Toss(1.0 * n * x[1] / total)]

def WeightedChoice(choices):
  """Choices is an iterable of 2-tuples, where the second value is the weight.
     Chooses one.
  """
  choices = list(choices)  # Needed since we iterate twice over the iterable.
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
  total = sum(weight for item, weight in choices)
  while total > 0:
    random_val = random.uniform(0, total)
    upto = 0
    for idx, ch in enumerate(choices):
      item, weight = ch
      if upto + weight > random_val:
        total -= weight
        choices = choices[0:idx] + choices[idx + 1:]
        yield item
        continue
      upto += weight

def Squash(val, cap):
  """Use a sigmoidal squashing function to squash to 100."""
  if val < 1:
    return val
  return cap * val / (cap - 1.0 + val)
