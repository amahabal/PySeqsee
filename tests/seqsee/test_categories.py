import unittest
from farg.category import Binding, CategorizableMixin, Category
from apps.seqsee.categories import Ascending, Prime, SizeNCategory
from apps.seqsee.mapping import NumericMapping, StructuralMapping
from apps.seqsee.sobject import SAnchored, SElement, SObject

class TestSeqseeCategories(unittest.TestCase):
  def test_sanity(self):
    self.assertTrue(issubclass(SObject, CategorizableMixin))

  def test_prime(self):
    self.assertTrue(Prime.IsInstance(SObject.Create(3)))
    self.assertFalse(Prime.IsInstance(SObject.Create(4)))
    self.assertFalse(Prime.IsInstance(SObject.Create(3, 5)))

    element = SObject.Create(17)
    binding = Prime.IsInstance(element)
    self.assertFalse(element.IsKnownAsInstanceOf(Prime))
    self.assertTrue(binding)
    self.assertEqual(6, binding.GetBindingsForAttribute('index'))

    binding2 = element.DescribeAs(Prime)
    self.assertTrue(element.IsKnownAsInstanceOf(Prime))
    self.assertTrue(binding2)
    self.assertEqual(6, binding2.GetBindingsForAttribute('index'))
    self.assertNotEqual(binding, binding2)

    # Same (stored) binding returned.
    binding3 = element.DescribeAs(Prime)
    self.assertEqual(binding3, binding2)

    element5 = SObject.Create(5)
    element7 = SObject.Create(7)
    element11 = SObject.Create(11)
    mapping = Prime.GetMapping(element5, element7)
    self.assertTrue(isinstance(mapping, NumericMapping))
    self.assertEqual(Prime, mapping.category)
    self.assertEqual("succ", mapping.name)

    self.assertEqual(11, mapping.Apply(element7).magnitude)

  def test_ascending(self):
    self.assertTrue(Ascending.IsInstance(SObject.Create(3)))
    self.assertTrue(Ascending.IsInstance(SObject.Create(3, 4, 5)))

    self.assertFalse(Ascending.IsInstance(SObject.Create(4, 6)))
    self.assertFalse(Ascending.IsInstance(SObject.Create(4, (5, 6))))

    group = SObject.Create(3, 4, 5)
    binding = Ascending.IsInstance(group)
    self.assertFalse(group.IsKnownAsInstanceOf(Ascending))
    self.assertTrue(binding)
    self.assertEqual(3, binding.GetBindingsForAttribute('start').magnitude)
    self.assertEqual(5, binding.GetBindingsForAttribute('end').magnitude)

    binding2 = group.DescribeAs(Ascending)
    self.assertTrue(group.IsKnownAsInstanceOf(Ascending))
    self.assertTrue(binding2)
    self.assertEqual(3, binding2.GetBindingsForAttribute('start').magnitude)
    self.assertNotEqual(binding, binding2)

    # Same (stored) binding returned.
    binding3 = group.DescribeAs(Ascending)
    self.assertEqual(binding3, binding2)

    element5 = SObject.Create(3, 4, 5)
    element7 = SObject.Create(3, 4, 5, 6)
    mapping = Ascending.GetMapping(element5, element7)
    self.assertTrue(isinstance(mapping, StructuralMapping))
    self.assertEqual(Ascending, mapping.category)

    self.assertEqual((3, 4, 5, 6, 7), mapping.Apply(element7).Structure())

  def test_sizen(self):
    Size2 = SizeNCategory.Create(size=2)
    Size2p = SizeNCategory.Create(size=2)
    Size3 = SizeNCategory.Create(size=3)

    self.assertEqual(Size2, Size2p)
    self.assertNotEqual(Size2, Size3)

    self.assertTrue(Size2.IsInstance(SObject.Create(3, 4)))
    self.assertTrue(Size2.IsInstance(SObject.Create(3, 5)))
    self.assertTrue(Size2.IsInstance(SObject.Create(3, (4, 5))))
    self.assertFalse(Size2.IsInstance(SObject.Create(3, 4, 6)))

    group = SObject.Create(3, 5)
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

    element5 = SObject.Create(3, 5)
    element6 = SObject.Create(3, 6)
    mapping = Size2.GetMapping(element5, element6)
    self.assertTrue(isinstance(mapping, StructuralMapping))
    self.assertEqual(Size2, mapping.category)

    self.assertEqual((3, 7), mapping.Apply(element6).Structure())
