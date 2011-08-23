from nose.tools import raises
from group import Group
from integer import Integer
from workspace import *

def test_elements():
  ws = Workspace()
  assert 0 == ws.ElementsCount()
  
  ws.AddElements(1, 1, 2, 1, 2, 3, 1, 2, 3, 4)
  assert 10 == ws.ElementsCount()
  
  ov = ws._AddOverlay(Group.QuickCreate(1, 2), 6, 8)
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
  
def test_get_overlays():
  ws = Workspace()
  ws.AddElements(1, 1, 2, 1, 2, 3, 1, 2, 3, 4)
  ws._AddOverlay('a', 0, 2)
  ws._AddOverlay('b', 0, 3)
  ws._AddOverlay('c', 1, 4)
  ws._AddOverlay('d1', 3, 4)
  
  assert set('a') == ws.GetOverlays(Equals(0), Equals(2))
  assert set(['c', 'd1']) == ws.GetOverlays(None, Equals(4))
  assert set(['a', 'b', 'c', 'd1']) == ws.GetOverlays(None, None)
  assert set(['b', 'c', 'd1']) == ws.GetOverlays(None, GreaterThanEq(3))
  assert set(['c', 'd1']) == ws.GetOverlays(None, GreaterThan(3))
  assert set(['d1']) == ws.GetOverlays(None, GreaterThan(3),
                                     (lambda (x): x.item.endswith('1')))
  
  assert set([]) == ws.GetOverlaysOverlapping(5, 6)
  assert set([]) == ws.GetOverlaysOverlapping(4, 5)
  assert set(['c', 'd1']) == ws.GetOverlaysOverlapping(3, 4)
  assert set(['c', 'd1']) == ws.GetOverlaysOverlapping(3, 6)
  assert set(['b', 'c', 'd1']) == ws.GetOverlaysOverlapping(2, 6)
  assert set(['b', 'c']) == ws.GetOverlaysOverlapping(2, 3)
