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

"""
Collects stats for multiple run with a single setting.
"""

from collections import defaultdict

def mean(numbers):
  if not numbers:
    return 0
  return sum(numbers) / len(numbers)

def median(numbers):
  l = len(numbers)
  n = sorted(numbers)
  if l % 2 == 0:
    return (n[int(l / 2)] + n[int(l / 2) - 1]) / 2.0
  else:
    return n[int((l - 1) / 2)]

class StatsForSingleState:
  """Stats for a single state (e.g., "SuccessfulCompletion") of a single run."""
  def __init__(self):
    self.codelet_counts = []

  def AddData(self, *, codelet_count):
    """
    Adds codelet count to data.
    @param codelet_count: Number of steps needed to reach this state. Can be 0 if it makes
       no sense for that state.
    """
    self.codelet_counts.append(codelet_count)

  def __str__(self):
    counts = sorted(self.codelet_counts)
    return 'Count: %d, Avg: %.2f, Min: %.2f, Max: %.2f, Median: %.2f, %s' % (len(counts),
                                                                             mean(counts),
                                                                             min(counts),
                                                                             max(counts),
                                                                             median(counts),
                                                                             counts)

class RunStats:
  """
  Stats for multiple runs with a single setting.
  """
  def __init__(self):
    self.stats_per_state = defaultdict(StatsForSingleState)

  def AddData(self, data_string):
    """
    Add a data point.
    @param data_string: Consists of a status (say, SuccessfulCompletion), optionally
       followed by the codelet count when that happened.
    """
    pieces = data_string.split()
    if len(pieces) == 1:
      self.stats_per_state[pieces[0]].AddData(codelet_count=0)
    else:
      self.stats_per_state[pieces[0]].AddData(codelet_count=int(pieces[1]))

  def __str__(self):
    """
    Printable version of stats.
    """
    individual_strings = ('%s: %s' % (k, str(v)) for k, v in self.stats_per_state.items())
    return "\n".join(individual_strings)
