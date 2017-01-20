from farg.apps.seqsee.categories import Ascending, MappingBasedCategory, Number, Prime, SizeNCategory
from farg.apps.seqsee.mapping import NumericMapping, StructuralMapping
from farg.apps.seqsee.sobject import SObject
from farg.core.categorization.categorizable import CategorizableMixin
import unittest
from farg.core.ltm.graph import LTMGraph
from farg.core.controller import Controller
from farg.core.ui.batch_ui import BatchUI
from farg.apps.seqsee.testing_utils import MockSeqseeController

class TestSeqseeCategories(unittest.TestCase):
  def test_sanity(self):
    self.assertTrue(issubclass(SObject, CategorizableMixin))

  def test_Prime(self):
    self.assertEqual(Prime(), Prime())
    self.assertTrue(Prime().IsInstance(SObject.Create([3])))
    self.assertFalse(Prime().IsInstance(SObject.Create([4])))
    self.assertFalse(Prime().IsInstance(SObject.Create([3, 5])))

    element = SObject.Create([17])
    binding = Prime().IsInstance(element)
    self.assertFalse(element.IsKnownAsInstanceOf(Prime()))
    self.assertTrue(binding)
    self.assertEqual(6, binding.GetBindingsForAttribute('index'))

    binding2 = element.DescribeAs(Prime())
    self.assertTrue(element.IsKnownAsInstanceOf(Prime()))
    self.assertTrue(binding2)
    self.assertEqual(6, binding2.GetBindingsForAttribute('index'))
    self.assertNotEqual(binding, binding2)

    # Same (stored) binding returned.
    binding3 = element.DescribeAs(Prime())
    self.assertEqual(binding3, binding2)

    element5 = SObject.Create([5])
    element7 = SObject.Create([7])
    mapping = Prime().GetMapping(element5, element7)
    self.assertTrue(isinstance(mapping, NumericMapping))
    self.assertEqual(Prime(), mapping.category)
    self.assertEqual("succ", mapping.name)

    self.assertEqual(11, mapping.Apply(element7).magnitude)

  def test_ascending(self):
    self.assertTrue(Ascending().IsInstance(SObject.Create([3])))
    self.assertTrue(Ascending().IsInstance(SObject.Create([3, 4, 5])))

    self.assertFalse(Ascending().IsInstance(SObject.Create([4, 6])))
    self.assertFalse(Ascending().IsInstance(SObject.Create([4, (5, 6)])))

    group = SObject.Create([3, 4, 5])
    binding = Ascending().IsInstance(group)
    self.assertFalse(group.IsKnownAsInstanceOf(Ascending()))
    self.assertTrue(binding)
    self.assertEqual(3, binding.GetBindingsForAttribute('start').magnitude)
    self.assertEqual(5, binding.GetBindingsForAttribute('end').magnitude)

    binding2 = group.DescribeAs(Ascending())
    self.assertTrue(group.IsKnownAsInstanceOf(Ascending()))
    self.assertTrue(binding2)
    self.assertEqual(3, binding2.GetBindingsForAttribute('start').magnitude)
    self.assertNotEqual(binding, binding2)

    # Same (stored) binding returned.
    binding3 = group.DescribeAs(Ascending())
    self.assertEqual(binding3, binding2)

    element5 = SObject.Create([13, 14, 15])
    element7 = SObject.Create([13, 14, 15, 16])
    _ui = BatchUI(controller_class=Controller)
    controller = _ui.controller
    controller.ltm = LTMGraph()
    mapping = Ascending().FindMapping(element5, element7, controller=controller,
                                      seqsee_ltm=controller.ltm)
    self.assertTrue(isinstance(mapping, StructuralMapping))
    self.assertEqual(Ascending(), mapping.category)

    self.assertEqual((13, 14, 15, 16, 17), mapping.Apply(element7).Structure())

  def test_sizen(self):
    Size2 = SizeNCategory(size=2)
    Size2p = SizeNCategory(size=2)
    Size3 = SizeNCategory(size=3)

    self.assertEqual(Size2, Size2p)
    self.assertNotEqual(Size2, Size3)

    self.assertTrue(Size2.IsInstance(SObject.Create([3, 4])))
    self.assertTrue(Size2.IsInstance(SObject.Create([3, 5])))
    self.assertTrue(Size2.IsInstance(SObject.Create([3, (4, 5)])))
    self.assertFalse(Size2.IsInstance(SObject.Create([3, 4, 6])))

    group = SObject.Create([3, 5])
    binding = Size2.IsInstance(group)
    self.assertFalse(group.IsKnownAsInstanceOf(Size2))
    self.assertTrue(binding)
    self.assertEqual(3, binding.GetBindingsForAttribute('pos_1').magnitude)
    self.assertEqual(5, binding.GetBindingsForAttribute('pos_2').magnitude)

    binding2 = group.DescribeAs(Size2)
    self.assertTrue(group.IsKnownAsInstanceOf(Size2))
    self.assertTrue(binding2)
    self.assertEqual(3, binding2.GetBindingsForAttribute('pos_1').magnitude)
    self.assertNotEqual(binding, binding2)

    # Same (stored) binding returned.
    binding3 = group.DescribeAs(Size2)
    self.assertEqual(binding3, binding2)

    element5 = SObject.Create([3, 5])
    element6 = SObject.Create([3, 6])
    _ui = BatchUI(controller_class=Controller)
    controller = _ui.controller
    controller.ltm = LTMGraph()
    mapping = Size2.FindMapping(element5, element6,
                                controller=controller,
                                seqsee_ltm=controller.ltm)
    self.assertTrue(isinstance(mapping, StructuralMapping))
    self.assertEqual(Size2, mapping.category)

    self.assertEqual((3, 7), mapping.Apply(element6).Structure())

  def test_mapping_based(self):
    Size2 = SizeNCategory(size=2)
    numeric_sameness = NumericMapping(name="same", category=Number())
    numeric_successor = NumericMapping(name="succ", category=Number())
    mapping_second_succ = StructuralMapping(
        category=Size2,
        bindings_mapping=frozenset((('pos_1', numeric_sameness),
                                    ('pos_2', numeric_successor))))
    mapping_first_succ = StructuralMapping(
        category=Size2,
        bindings_mapping=frozenset((('pos_2', numeric_sameness),
                                    ('pos_1', numeric_successor))))
    SecondSucc = MappingBasedCategory(mapping=mapping_second_succ)
    SecondSuccp = MappingBasedCategory(mapping=mapping_second_succ)
    FirstSucc = MappingBasedCategory(mapping=mapping_first_succ)

    self.assertEqual(SecondSucc, SecondSuccp)
    self.assertNotEqual(SecondSucc, FirstSucc)

    self.assertTrue(SecondSucc.IsInstance(SObject.Create([(3, 4), (3, 5)])))
    self.assertTrue(SecondSucc.IsInstance(SObject.Create([3, 5])))
    self.assertTrue(SecondSucc.IsInstance(SObject.Create([(3, 4), (3, 5), (3, 6)])))
    self.assertFalse(SecondSucc.IsInstance(SObject.Create([3, 4, 6])))
    self.assertFalse(SecondSucc.IsInstance(SObject.Create([(3, 4), (3, 6), (3, 7)])))

    group = SObject.Create([(3, 5), (3, 6)])
    binding = SecondSucc.IsInstance(group)
    self.assertFalse(group.IsKnownAsInstanceOf(SecondSucc))
    self.assertTrue(binding)
    self.assertEqual((3, 5), binding.GetBindingsForAttribute('start').Structure())
    self.assertEqual(2, binding.GetBindingsForAttribute('length').magnitude)

    binding2 = group.DescribeAs(SecondSucc)
    self.assertTrue(group.IsKnownAsInstanceOf(SecondSucc))
    self.assertTrue(binding2)
    self.assertEqual((3, 5), binding.GetBindingsForAttribute('start').Structure())
    self.assertEqual(2, binding.GetBindingsForAttribute('length').magnitude)
    self.assertNotEqual(binding, binding2)

    # Same (stored) binding returned.
    binding3 = group.DescribeAs(SecondSucc)
    self.assertEqual(binding3, binding2)

    element5 = SObject.Create([(13, 5), (13, 6)])
    element6 = SObject.Create([(14, 6), (14, 7), (14, 8)])
    controller = MockSeqseeController()
    mapping = SecondSucc.FindMapping(element5, element6,
                                     controller=controller,
                                     seqsee_ltm=controller.ltm)
    self.assertTrue(isinstance(mapping, StructuralMapping))
    self.assertEqual(SecondSucc, mapping.category)

    self.assertEqual(((15, 7), (15, 8), (15, 9), (15, 10)), mapping.Apply(element6).Structure())

