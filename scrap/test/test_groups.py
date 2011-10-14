from nose.tools import raises
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

@raises(Exception)
def test_no_repetitions():
  a = Integer(7)
  Group(a, a)
  
@raises(Exception)
def test_no_repetitions2():
  a = Integer(7)
  Group(Group(Integer(5), a), Group(Integer(5), a))
  
def test_meto():
  g = Group.QuickCreate(1, (2, 2), 3, 4, 5)
  m = Group.QuickCreate(1, 2, 3, 4, 5)
  i = Integer(2)
  r = Integer(4)
  t = Integer(2)
  
  assert not g.HasMetonym()
  assert g.TerminalMetonym() == g
  
  g.SetMetonym(m)
  assert g.HasMetonym()
  assert g.Metonym() == m
  assert g.TerminalMetonym() == m
  
  r.SetMetonym(t)
  m.SetMetonym(r)
  assert g.TerminalMetonym() == t
  
  g[1].SetMetonym(i)
  assert g.TerminalMetonym() == t
  assert g[1].TerminalMetonym() == i
  
def test_Structure():
  i = Integer(7)
  assert i.Structure() == 7
  
  g = Group.QuickCreate(7)
  assert g.Structure() == (7, )
  
  g = Group.QuickCreate(5, [7, 7], 9)
  assert g.Structure() == (5, (7, 7), 9)