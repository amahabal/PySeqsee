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

"""General utilities."""

import colorsys
import random


def hsv_to_color_string(hue, saturation, value):
    """Convert from HSV to RGB color space."""
    rgb = ('%02x' % (255.0 * x) for x in colorsys.hsv_to_rgb(hue, saturation, value))
    return '#' + ''.join(rgb)


def toss(x):
    """x is a number between 0 and 1. Returns true with probability x."""
    return random.uniform(0, 1) <= x


def choose_about_n(n, choices):
    """Choose in a way that the expected number of choices is n.

    Args:
      n: The expected number of responses.
      choices: an iterable of 2-tuples, where the second value is the weight.

    An example to show how it works: let choices contain 5 things with weights 10, 20, 30
    40, and 50 (thus summing to 150), and let n=3. Then we will keep the first item in the
    output with probability 3 * 10/150 (i.e., 20%).

    Returns:
      A list of a roughly n-sized subset of choices.
    """
    choices = list(choices)  # Needed since we iterate twice over the iterable.
    total = sum(w for _c, w in choices)
    return [x[0] for x in choices if toss(1.0 * n * x[1] / total)]


def weighted_choice(choices):
    """Chooses an item, biased by weight.

    Args:
     choices: an iterable of 2-tuples, where the second value is the weight.

    Returns:
      An element of choices.
    """
    choices = list(choices)  # Needed since we iterate twice over the iterable.
    total = sum(weight for item, weight in choices)
    random_sum = random.uniform(0, total)
    upto = 0
    for item, weight in choices:
        if upto + weight > random_sum:
            return item
        upto += weight
    assert False, "Shouldn't get here"


def select_weighted_by_activation(ltm, choices):
    """Given an ltm and nodes in ltm, chooses one biased by activation."""
    choices = ((x, ltm.GetNode(content=x).GetActivation(current_time=0)) for x in choices)
    return weighted_choice(choices)


def unweighted_choice(choices):
    """Chooses one item uniformly randomly from is an iterable."""
    choices = list(choices)  # Needed since we need to choose nth element and need length.
    random_choice = random.uniform(0, len(choices))
    return choices[int(random_choice)]


def weighted_shuffle(choices):
    """Shuffle items by weight.

    Args:
      choices: an iterable of 2-tuples, where the second value is the weight.

    Yields:
       Repeatedly yields first elements of the 2-tuple, resulting, when complete, in a shuffle.
    """
    total = sum(weight for item, weight in choices)
    while total > 0:
        random_val = random.uniform(0, total)
        upto = 0
        for idx, choice in enumerate(choices):
            item, weight = choice
            if upto + weight > random_val:
                total -= weight
                choices = choices[0:idx] + choices[idx + 1:]
                yield item
                continue
            upto += weight


def squash(val, cap):
    """Use a sigmoidal squashing function to squash to 100."""
    if val < 1:
        return val
    return cap * val / (cap - 1.0 + val)
