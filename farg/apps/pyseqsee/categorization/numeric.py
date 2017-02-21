from farg.apps.pyseqsee.categorization.categories import PSCategory
from farg.apps.pyseqsee.categorization.logic import InstanceLogic, Verify
from farg.apps.pyseqsee.objects import PSElement

class CategoryEvenInteger(PSCategory):
  _Rules = ('_mag: _INSTANCE.magnitude', '_half: _mag / 2', 'half: PSElement(magnitude=_half)')
  _Checks = ('_mag % 2 == 0', )
  _Constructors =  {('_mag', ): (lambda _mag: PSElement(magnitude=_mag))}
  _Attributes = set(('half', ))
  _Context = dict(PSElement=PSElement)
  _TurnedOffAttributes = set(('half', ))

  def BriefLabel(self):
    return "CategoryEvenInteger"

class PrecomputedListNumericCategory(PSCategory):
  _Constructors =  {('_mag', ): (lambda _mag: PSElement(magnitude=_mag))}
  _Rules = ('_mag: _INSTANCE.magnitude', )
  _Checks = ('_mag in number_list', )

  def __init__(self):
    self._Context = dict(number_list=self._number_list)
    PSCategory.__init__(self)

class CategoryPrime(PrecomputedListNumericCategory):
  _number_list = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
                  83, 89, 97)

  def BriefLabel(self):
    return "Primes"
