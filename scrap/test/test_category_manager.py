from nose.tools import raises
from category_manager import CategoryManager

def test_sanity():
  c = CategoryManager()
  c.AddAttribute('foo', 3)
  assert 3 == c.GetAttribute('foo')
  assert 3 == c.GetAttribute('foo', ns='Global')
  
def test_namespace_sanity():
  c = CategoryManager()
  i = ()
  c.AddAttribute('bar', 4, ns=i)
  assert 4 == c.GetAttribute('bar', ns=i)
  assert not(c.HasAttribute('bar'))
  assert c.HasAttribute('bar', ns=i)
  
def test_namespace_shadowing():
  c = CategoryManager()
  i = ()
  c.AddAttribute('bar', 4, ns=i)
  c.AddAttribute('bar', 5)
  assert 4 == c.GetAttribute('bar', ns=i)
  assert 5 == c.GetAttribute('bar')

def test_inheritance_from_global():
  c = CategoryManager()
  c.AddAttribute('foo', 3)
  i = ()
  assert 3 == c.GetAttribute('foo', ns=i)

@raises(Exception)
def test_raises_when_no_att():
  c = CategoryManager()
  c.GetAttribute('foo')
  
def test_get_bindings():
  c = CategoryManager()
  c.AddAttribute('foo', 3)
  c.AddAttribute('bat', 4)
  i = ()
  c.AddAttribute('bar', 5, ns=i)
  c.AddAttribute('bat', 6, ns=i)
  
  b = c.GetBindings()
  assert 3 == b['foo']
  assert 4 == b['bat']
  
  b = c.GetBindings(i)
  assert 3 == b['foo']
  assert 5 == b['bar']
  assert 6 == b['bat']
  
def test_can_non_cat():
  c = CategoryManager()
  i = (1, )
  j = (2, )
  k = (3, )
  c.MarkAsInstance(i)
  c.MarkAsNonInstance(j)
  
  assert c.IsKnownInstanceOf(i)
  assert not c.IsKnownNonInstanceOf(i)
  
  assert not c.IsKnownInstanceOf(j)
  assert c.IsKnownNonInstanceOf(j)
  
  assert not c.IsKnownInstanceOf(k)
  assert not c.IsKnownNonInstanceOf(k)
  