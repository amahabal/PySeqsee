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

def Mean(numbers):
  """Returns the average of the input, 0 if empty."""
  if not numbers:
    return 0
  return sum(numbers) / len(numbers)

def Median(numbers):
  """Returns the median of the input, 0 if empty."""
  length = len(numbers)
  if length == 0:
    return 0
  sorted_numbers = sorted(numbers)
  if length % 2 == 0:
    return (sorted_numbers[int(length / 2)] + sorted_numbers[int(length / 2) - 1]) / 2.0
  else:
    return sorted_numbers[int((length - 1) / 2)]

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
                                                                             Mean(counts),
                                                                             min(counts),
                                                                             max(counts),
                                                                             Median(counts),
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
    if data_string.decode('utf-8').startswith('ERROR'):
      self.stats_per_state['ERROR'].AddData(codelet_count=0)
      print("========\n%s\n====" % data_string.decode('utf-8'))
      return
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

class AllStats:
  """Stats for all inputs for each iteration thus far."""
  def __init__(self, *, left_name, right_name):
    """
    Initialize stats. The names will typically be "Base" and "Expt", or "Previous" and
    "Current".
    """
    self.left_name = left_name
    self.right_name = right_name

    #: Order in which inputs have been seen.
    self.input_order = []

    #: Stats for the left side.
    self.left_stats = defaultdict(RunStats)

    #: Stats for the right side.
    self.right_stats = defaultdict(RunStats)

  def GetLeftStatsFor(self, input):
    """Get left stats for input. Create (empty) if not present."""
    if input not in self.input_order:
      self.input_order.append(input)
    return self.left_stats[input]

  def GetRightStatsFor(self, input):
    """Get right stats for input. Create (empty) if not present."""
    if input not in self.input_order:
      self.input_order.append(input)
    return self.right_stats[input]
