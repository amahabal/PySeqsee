import random

class Coderack:
  def __init__(self, max_capacity):
    self._max_capacity = max_capacity
    self._urgency_sum = 0
    self._codelet_count = 0
    self._codelets = set()
    
  def IsEmpty(self):
    return (self._codelet_count == 0)
  
  def GetCodelet(self):
    if self._codelet_count == 0:
      raise Exception("Coderack empty")
    random_urgency = random.uniform(0, self._urgency_sum)
    for codelet in self._codelets:
      if codelet.urgency >= random_urgency:
        self._RemoveCodelet(codelet)
        return codelet
      else:
        random_urgency -= codelet.urgency
        
  def AddCodelet(self, codelet):
    if self._codelet_count == self._max_capacity:
      self._ExpungeSomeCodelet()
    self._codelets.add(codelet)
    self._codelet_count += 1
    self._urgency_sum += codelet.urgency
      
  def _RemoveCodelet(self, codelet):
    self._codelets.remove(codelet)
    self._codelet_count -= 1
    self._urgency_sum -= codelet.urgency
    
  def _ExpungeSomeCodelet(self):
    # TODO(amahabal): Which one? Choosing randomly...
    codelet = random.choice(list(self._codelets))
    self._RemoveCodelet(codelet)