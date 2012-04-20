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
The Coderack in Seqsee is like a todo list.  It consists of promising 
actions to take next, each associated with a number indicating the degree 
of promise.  Seqsee chooses an item and runs it, and in that process of 
running it may come up with other promising actions that are then added to 
the Coderack.  

The probability of choosing an item depends on its promise.  Higher 
promise actions are likelier to be chosen, but it is still possible for 
ignore promise actions to occasionally get chosen.  

Each action is called a codelet.  As that term suggests, the action is a 
tiny and targeted.  In fact, Seqsee requires several dozens of codelets to 
understand even simple sequences.  

Just as the contents of a person's to do list can strongly suggest their 
actions over the next few hours, the Coderack's contents indicate the 
directions Seqsee will pursue in the near future.
"""
import random
from farg.core.exceptions import FargError, FargException

import logging
logger = logging.getLogger(__name__)


class CoderackEmptyException(FargException):
  """Raised if :func:`~Coderack.GetCodelet` called on an empty coderack."""
  pass

class Coderack(object):
  """Implements the coderack --- the collection of codelets waiting to run.
  
  .. todo:: Choose the codelet to expunge based on a better criteria than uniformly randomly.
  """

  def __init__(self, max_capacity):
    #: Maximum number of codelets that the coderack can hold.
    self._max_capacity = max_capacity
    #: Sum of urgencies of all codelets in coderack.
    self._urgency_sum = 0
    #: Number of codelets present.
    self._codelet_count = 0
    #: The set of codelets.
    self._codelets = set()
    #: For testing, it is useful to be able to force next codelet to return.
    self._forced_next_codelet = None

  def CodeletCount(self):
    return self._codelet_count

  def IsEmpty(self):
    """True if contains no codelets."""
    return (self._codelet_count == 0)

  def GetCodelet(self):
    """Randomly selects a codelet (biased by urgency).
       Requires the coderack to be nonempty.
    """
    if self._forced_next_codelet:
      codelet = self._forced_next_codelet
      self._RemoveCodelet(codelet)
      self._forced_next_codelet = None
      return codelet
    if self._codelet_count == 0:
      raise CoderackEmptyException()
    random_urgency = random.uniform(0, self._urgency_sum)
    # The following loop is guarenteed to terminate.
    for codelet in self._codelets:
      if codelet.urgency >= random_urgency:
        self._RemoveCodelet(codelet)
        return codelet
      else:
        random_urgency -= codelet.urgency

  def AddCodelet(self, codelet):
    """Adds codelet to coderack. Removes some existing codelet if needed."""
    logger.debug('Codelet added: %s', str(codelet.family))
    if self._codelet_count == self._max_capacity:
      self._ExpungeSomeCodelet()
    self._codelets.add(codelet)
    self._codelet_count += 1
    self._urgency_sum += codelet.urgency

  def ForceNextCodelet(self, codelet):
    """Force codelet to be the next one retrieved by GetCodelet.
    
     .. Note::
    
        This mechanism should only be used during testing. It is unsafe in that if the
        codelet is expunged (because of new codelets being added), the program can crash.
        This will never happen if the next codelet is marked and GetCodelet called soon
        thereafter.
    """
    if codelet not in self._codelets:
      raise FargError("Cannot mark a non-existant codelet as the next to retrieve.")
    self._forced_next_codelet = codelet

  def _RemoveCodelet(self, codelet):
    """Removes named codelet from coderack."""
    self._codelets.remove(codelet)
    self._codelet_count -= 1
    self._urgency_sum -= codelet.urgency

  def _ExpungeSomeCodelet(self):
    """Removes a codelet, chosen uniformly randomly."""
    codelet = random.choice(list(self._codelets))
    logger.info('Coderack over capacity: expunged codelet of family %s.' %
                codelet.family.__name__)
    self._RemoveCodelet(codelet)
