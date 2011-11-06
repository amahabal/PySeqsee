import unittest
from farg.category import Binding, CategorizableMixin, Category
from apps.seqsee.categories import Prime
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
