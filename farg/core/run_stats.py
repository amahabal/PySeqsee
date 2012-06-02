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
from math import sqrt

def Mean(numbers):
  """Returns the average of the input, 0 if empty."""
  if not numbers:
    return 0
  return sum(numbers) / len(numbers)

def Variance(numbers):
  assert(len(numbers) >= 2)
  count = len(numbers)
  mean = sum(numbers) / count
  return sum((x - mean) * (x - mean) for x in numbers) / count

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
    self.count = 0
    self.successful_codelet_count = 0

  def IsEmpty(self):
    """Returns true if no data has been added."""
    return not bool(self.stats_per_state)

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
    self.count = self.count + 1
    if pieces[0] == b'SuccessfulCompletion':
      self.successful_codelet_count = self.successful_codelet_count + 1

  def __str__(self):
    """
    Printable version of stats.
    """
    individual_strings = ('%s: %s' % (k, str(v)) for k, v in self.stats_per_state.items())
    return "\n".join(individual_strings)

def Descriptor(*, t, df, less="Less", more="More"):
  """Given t and degrees of freedom, returns "More", "Less", or "", at roughtly 95%
     confidence.
  """
  if df < 5:
    return ""
  if df < 10:
    if abs(t) > 2.3:
      return more if t > 0 else less
    return ""
  if df < 20:
    if abs(t) > 2.1:
      return more if t > 0 else less
    return ""
  if abs(t) > 1.98:
    return more if t > 0 else less
  return ""



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

    #: Memoized Stats
    self.memoized_stats = defaultdict(tuple)

  def GetTStatsDict(self, left_numbers, right_numbers):
    n1 = len(left_numbers)
    n2 = len(right_numbers)
    left_mean = Mean(left_numbers) if n1 else 0
    right_mean = Mean(right_numbers) if n2 else 0
    left_variance = Variance(left_numbers) if n1 > 1 else 0
    right_variance = Variance(right_numbers) if n2 > 1 else 0
    df = n1 + n2 - 2
    svar = ((n1 - 1) * left_variance + (n2 - 1) * right_variance) / float(df) if df else 0
    if svar and n1 and n2:
      t = (right_mean - left_mean) / sqrt(svar * (1.0 / n1 + 1.0 / n2))
    else:
      t = 0
    return  dict(left_mean=left_mean,
                 right_mean=right_mean,
                 left_variance=left_variance,
                 right_variance=right_variance,
                 n1=n1,
                 n2=n2,
                 df=df,
                 t=t)

  def GetComparitiveStats(self, for_input):
    left_stats = self.left_stats[for_input]
    right_stats = self.right_stats[for_input]
    memoized = self.memoized_stats[for_input]
    if memoized:
      left_count, right_count, codelet_stats, success_stats = memoized
      if left_count == left_stats.count and right_count == right_stats.count:
        return (codelet_stats, success_stats)
    left_successful_codelets = left_stats.stats_per_state[b'SuccessfulCompletion'].codelet_counts
    right_successful_codelets = right_stats.stats_per_state[b'SuccessfulCompletion'].codelet_counts
    codelet_count_stats = self.GetTStatsDict(left_successful_codelets,
                                             right_successful_codelets)
    descriptor = Descriptor(t=codelet_count_stats['t'],
                            df=codelet_count_stats['df'],
                            less="Faster", more="Slower")
    codelet_count_stats['descriptor'] = descriptor

    success_stats = self.GetTStatsDict([1 if x < len(left_successful_codelets) else 0
                                        for x in range(left_stats.count)],
                                       [1 if x < len(right_successful_codelets) else 0
                                        for x in range(right_stats.count)])
    descriptor = Descriptor(t=success_stats['t'],
                            df=success_stats['df'],
                            more="More Success", less="Less Success")
    success_stats['descriptor'] = descriptor
    self.memoized_stats[for_input] = (left_stats.count, right_stats.count,
                                      codelet_count_stats, success_stats)
    return (codelet_count_stats, success_stats)

  def IsRightBetter(self, for_input):
    codelet_count_stats, success_stats = self.GetComparitiveStats(for_input)
    if not codelet_count_stats:
      return ("", "")
    return (codelet_count_stats['descriptor'], success_stats['descriptor'])

  def GetLeftStatsFor(self, input_to_run):
    """Get left stats for input_to_run. Create (empty) if not present."""
    if input_to_run not in self.input_order:
      self.input_order.append(input_to_run)
    return self.left_stats[input_to_run]

  def GetRightStatsFor(self, input_to_run):
    """Get right stats for input_to_run. Create (empty) if not present."""
    if input_to_run not in self.input_order:
      self.input_order.append(input_to_run)
    return self.right_stats[input_to_run]
