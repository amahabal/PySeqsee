from farg.apps.pyseqsee.categorization.categories import PyCategory
from farg.apps.pyseqsee.categorization.logic import InstanceLogic, Verify
from farg.apps.pyseqsee.objects import PSElement

class CategoryEvenInteger(PyCategory):
  _rules = ('inst: Verify(inst, inst.magnitude % 2 == 0)',)
  _guessers = ('inst: instance.CopyByStructure()', )
  _external_vals = dict(Verify=Verify)
  _object_constructors =  {('inst', ): (lambda inst: inst)}

  def BriefLabel(self):
    return "CategoryEvenInteger"

class PrecomputedListNumericCategory(PyCategory):
  _guessers = ('inst: instance.CopyByStructure()', )
  _object_constructors =  {('inst', ): (lambda inst: inst)}

  def __init__(self):
    self._rules = ('inst: Verify(inst, inst.magnitude in number_list)', )
    self._external_vals = dict(Verify=Verify, number_list=self._number_list)
    PyCategory.__init__(self)

class CategoryPrime(PrecomputedListNumericCategory):
  _number_list = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
                  83, 89, 97)

  def BriefLabel(self):
    return "Primes"
