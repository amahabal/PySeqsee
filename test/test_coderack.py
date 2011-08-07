from coderack import Coderack

class MockCodelet(object):
  def __init__(self, urgency):
    self.urgency = urgency

def test_basic():
  c = Coderack(10)
  assert 10 == c._max_capacity
  c.AddCodelet(MockCodelet(20))
  assert 1 == c._codelet_count
  assert 20 == c._urgency_sum
  
  c._ExpungeSomeCodelet()
  assert 0 == c._codelet_count
  assert 0 == c._urgency_sum
  