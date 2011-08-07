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
