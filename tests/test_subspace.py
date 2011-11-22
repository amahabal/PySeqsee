import random
import unittest

from apps.seqsee.sobject import SObject
from apps.seqsee.categories import Ascending, GetMapping
from apps.seqsee.mapping import StructuralMapping
from apps.seqsee.util import WeightedShuffle
from farg.codelet import Codelet, CodeletFamily
from farg.controller import Controller
from farg.exceptions import FargException, AnswerFoundException, NoAnswerException
from farg.runstate import RunState

import logging
logger = logging.getLogger(__name__)

def AnswerFound(answer):
  return { 'answer_found': True, 'answer': answer}

def NeedDeeperExploration():
  return { 'answer_found': False }

def NoAnswerLikely():
  return None

class Subspace(object):
  """A base class for subspaces."""

  @classmethod
  def QuickReconnaisance(cls, arguments):
    return NeedDeeperExploration()

  def __init__(self):
    self.runstate = RunState()
    self.controller = Controller(self.runstate)


class CF_NumericCase(CodeletFamily):
  @classmethod
  def Run(cls, runstate):
    ws = runstate.workspace
    v1 = ws.left
    v2 = ws.right
    if isinstance(v1, int) and isinstance(v2, int):
      diff_string = NumericMapping.DifferenceString(v1, v2)
      if diff_string:
        return NumericMapping(diff_string, Number)
      else:
        raise NoAnswerException()
    runstate.AddCodelet(CF_ChooseCategory, 100)

class CF_ChooseCategory(CodeletFamily):
  @classmethod
  def Run(cls, runstate):
    ws = runstate.workspace
    v1 = ws.left
    v2 = ws.right
    if not ws.category:
      common_categories = v1.GetCommonCategoriesSet(v2)
      if common_categories:
        # ... ToDo: Don't merely use the first category!
        cat = list(common_categories)[0]
        ws.category = cat
      else:
        raise NoAnswerException()
    runstate.AddCodelet(CF_GetBindings, 100)

class CF_GetBindings(CodeletFamily):
  @classmethod
  def Run(cls, runstate):
    ws = runstate.workspace
    v1 = ws.left
    v2 = ws.right
    category = ws.category
    b1 = v1.GetBindingsForCategory(category)
    if not b1:
      raise NoAnswerException()
    ws.b1 = b1
    b2 = v2.GetBindingsForCategory(category)
    if not b2:
      raise NoAnswerException()
    ws.b2 = b2
    ws.attribute_explanations = {}
    runstate.AddCodelet(CF_ExplainValues, 100)

class CF_ExplainValues(CodeletFamily):
  @staticmethod
  def CreateStructuralMappingFromExplanation(category, explanation):
    slippages = {}
    mappings = {}
    for right_attribute, val in explanation.iteritems():
      left_attribute, mapping = val
      if left_attribute != right_attribute:
        slippages[right_attribute] = left_attribute
      mappings[right_attribute] = mappings
    return StructuralMapping(category, mappings, slippages)

  @classmethod
  def Run(cls, runstate):
    ws = runstate.workspace
    attribute_explanations = ws.attribute_explanations
    b2 = ws.b2
    b2_dict = b2.bindings
    unexplained_attributes = [x for x in b2_dict.keys() if x not in attribute_explanations]
    one_attribute = random.choice(unexplained_attributes)
    logger.info("Chose attribute %s for explanation.", one_attribute)
    attribute_value = b2_dict[one_attribute]
    logger.info("Will love to explain this value: %s", str(attribute_value.Structure()))

    # Pick an ordering of attributes (biased in some way... how, and how to implement bias?)
    # I wish there was a weighted choice in random :)
    b1 = ws.b1
    b1_dict = b1.bindings
    attributes_to_use = dict([(a, 1) for a in b1_dict.keys()])
    attributes_to_use[one_attribute] += 3
    for attribute_to_use in WeightedShuffle(attributes_to_use.items()):
      mapping = GetMapping(b1_dict[attribute_to_use], b2_dict[one_attribute])
      logger.info("Used %s, saw mapping %s", attribute_to_use, str(mapping))
      if mapping:
        attribute_explanations[one_attribute] = (attribute_to_use, mapping)
        if ws.category.AreAttributesSufficientToBuild(attribute_explanations.keys()):
          # We have an explanation...
          full_mapping = CF_ExplainValues.CreateStructuralMappingFromExplanation(
              ws.category, attribute_explanations)
          raise AnswerFoundException(full_mapping)
    runstate.AddCodelet(CF_ExplainValues, 100)


class SubspaceFindMapping(Subspace):
  class Workspace():
    def __init__(self, left, right, category):
      self.left = left
      self.right = right
      self.category = category

  def Initialize(self, arguments):
    self.workspace = self.runstate.workspace = self.Workspace(**arguments)
    logger.info('Initialized new subspace')
    self.runstate.AddCodelet(CF_NumericCase, 100)

  @classmethod
  def QuickReconnaisance(cls, arguments):
    if 'category' in arguments:
      mapping = arguments['category'].GetMapping(arguments['left'], arguments['right'])
    else:
      mapping = GetMapping(arguments['left'], arguments['right'])
    if mapping:
      return AnswerFound(mapping)
    return NeedDeeperExploration()

def Subtask(subspace_class, max_number_of_steps, arguments):
  """The driver for subtask calculations: creates a subspace based on class and arguments, and
  runs it to a maximum of max_number_of_steps, returning None or an appropriate result."""
  quick_result = subspace_class.QuickReconnaisance(arguments)
  if not quick_result:
    return None
  if quick_result['answer_found']:
    return quick_result['answer']
  if not max_number_of_steps:
    return None
  subspace = subspace_class()
  subspace.Initialize(arguments)
  try:
    subspace.controller.RunUptoNSteps(max_number_of_steps)
  except AnswerFoundException as e:
    return e.answer
  return None

class TestSubspace(unittest.TestCase):
  def test_sanity(self):
    # This test refers to things in the Seqsee app. Maybe the test should move there.
    a3 = SObject.Create(1, 2, 3)
    a4 = SObject.Create(1, 2, 3, 4)
    a5 = SObject.Create(1, 2, 3, 4, 5)

    a19_21 = SObject.Create(19, 20, 21)

    mapping = Subtask(SubspaceFindMapping, 3, { 'left': a3, 'right': a4, 'category': Ascending})
    self.assertTrue(isinstance(mapping, StructuralMapping))
    self.assertEqual(Ascending, mapping.category)
    self.assertEqual(None, mapping.slippages)

    mapping = Subtask(SubspaceFindMapping, 3, { 'left': a5,
                                                'right': a19_21,
                                                'category': Ascending})
    self.assertEqual(None, mapping)

  def test_with_slippages(self):
    a17_19 = SObject.Create(17, 18, 19)
    a19_21 = SObject.Create(19, 20, 21)

    mapping = Subtask(SubspaceFindMapping, 10, { 'left': a17_19,
                                                 'right': a19_21,
                                                 'category': Ascending})
    self.assertTrue(isinstance(mapping, StructuralMapping))
    self.assertEqual(Ascending, mapping.category)
    self.assertEqual('end', mapping.slippages['start'])
