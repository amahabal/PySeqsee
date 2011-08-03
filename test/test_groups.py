from group import Group
from integer import Integer

def test_integers():
  a = Integer(7)
  assert a.magnitude == 7
  
def test_groups():
  g = Group(Integer(7), Integer(8), Group(Integer(9), Integer(10)))
  assert 3 == g.size()
  assert 7 == g[0].magnitude
  assert 10 == g[2][1].magnitude
  
def test_quick_create():
  g = Group.QuickCreate(1, 2, [3, 3], 4, 5)
  assert 2 == g[2].size()
  assert 3 == g[2][0].magnitude
  assert 5 == g.size()