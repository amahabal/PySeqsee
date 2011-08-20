from nose.tools import raises
from group import Group
from integer import Integer
from workspace import Workspace, Overlay

def test_elements():
  ws = Workspace()
  assert 0 == ws.ElementsCount()
  
  ws.AddElements(1, 1, 2, 1, 2, 3, 1, 2, 3, 4)
  assert 10 == ws.ElementsCount()
  
  ov = ws.AddOverlay(Group.QuickCreate(1, 2), 6, 8)
  assert isinstance(ov, Overlay)
  assert 6 == ov.start
  assert 8 == ov.end
  assert 2 == ov.Length()
  
def test_aligns():
  ws = Workspace()
  ws.AddElements(1, 1, 2, 1, 2, 3, 1, 2, 3, 4)
  assert ws.AlignsWith(Integer(2), 4)
  assert not ws.AlignsWith(Integer(2), 5)
  
  assert ws.AlignsWith(Group.QuickCreate(1), 3)
  assert ws.AlignsWith(Group.QuickCreate([1]), 3)
  assert ws.AlignsWith(Group.QuickCreate(1, 2, 3), 3)