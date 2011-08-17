from nose.tools import raises
from group import Group
from integer import Integer
from stream import Stream

class MyFocusable(object):
  def __init__(self, x):
    self.x = x
    self.y = 2 * x

  def GetFringe(self):
    return { self.x: 0.7, self.y: 0.4 }
  
  
def test_basic():
  s = Stream()
  assert 0 == s.FociCount()
  
  m3 = MyFocusable(3)
  m6 = MyFocusable(6)
  
  hits_map = s.FocusOn(m3)
  assert 1 == s.FociCount()
  assert 0 == len(hits_map)

  hits_map = s.FocusOn(m3)
  assert 1 == s.FociCount()
  assert 0 == len(hits_map)

  hits_map = s.FocusOn(m6)
  assert 2 == s.FociCount()
  assert 1 == len(hits_map)
  assert m3 in hits_map
  assert abs(hits_map[m3] - 0.28) < 0.001

  