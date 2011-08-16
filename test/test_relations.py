from group import Group
from integer import Integer
from mapping import Mapping
from relation import Relation

from nose.tools import raises

class M(Mapping):
  realm = Integer
  arity = 1
  
  @staticmethod
  def fn(i):
    return Integer(i.magnitude + 1)
  
  @staticmethod
  def rev_fn(i):
    return Integer(i.magnitude - 1)

def test_basic():
  g = Group.QuickCreate(1, 2, 3)
  r = Relation(g[0], g[1], M)
  r2 = Relation(g[0], g[1], M)
  
  assert not g[0].IsRelatedTo(g[1])
  assert not r.ConflictsExisting()
  assert not r2.ConflictsExisting()

  r.Insert()

  assert g[0].IsRelatedTo(g[1])
  assert not r.ConflictsExisting()
  assert r2.ConflictsExisting()

  assert r == g[0].RelationTo(g[1])
  assert r == g[1].RelationTo(g[0])

  assert g[0].IsRelatedTo(g[1])
  assert g[1].IsRelatedTo(g[0])

  assert (r, ) == tuple(g[0].OutgoingRelations())
  assert (r, ) == tuple(g[1].IncomingRelations())

  assert (r, ) == tuple(g[0].Relations())
  assert (r, ) == tuple(g[1].Relations())
  
  assert ( ) == tuple(g[1].OutgoingRelations())
  assert ( ) == tuple(g[0].IncomingRelations())
  
  r.Uninsert()
  assert not r.ConflictsExisting()
  assert not r2.ConflictsExisting()
