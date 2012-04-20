# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

from farg.apps.seqsee.categories import GetNaiveMapping, Number
from farg.apps.seqsee.mapping import NumericMapping, StructuralMapping
from farg.apps.seqsee.relation import Relation
from farg.core.codelet import CodeletFamily
from farg.core.controller import Controller
from farg.core.exceptions import AnswerFoundException, NoAnswerException
from farg.core.subspace import QuickReconnResults, Subspace
from farg.core.util import WeightedShuffle, WeightedChoice
import logging
import random

# TODO(#53 --- Dec 29, 2011): Needs big fat documentation.

logger = logging.getLogger(__name__)


class CF_NumericCase(CodeletFamily):
  @classmethod
  def Run(cls, controller):
    ws = controller.workspace
    v1 = ws.left
    v2 = ws.right
    if isinstance(v1, int) and isinstance(v2, int):
      diff_string = NumericMapping.DifferenceString(v1, v2)
      if diff_string:
        return NumericMapping(name=diff_string, category=Number)
      else:
        raise NoAnswerException(codelet_count=controller.steps_taken)
    controller.AddCodelet(family=CF_ChooseCategory, urgency=100)

class CF_ChooseCategory(CodeletFamily):
  @classmethod
  def Run(cls, controller):
    ws = controller.workspace
    v1 = ws.left
    v2 = ws.right

    if not ws.category:
      common_categories = v1.GetCommonCategoriesSet(v2)
      if common_categories:
        # ... ToDo: Don't merely use the first category!
        cat = WeightedChoice((x, 1) for x in common_categories)
        ws.category = cat
      else:
        raise NoAnswerException(codelet_count=controller.steps_taken)
    controller.AddCodelet(family=CF_GetBindings, urgency=100)

class CF_GetBindings(CodeletFamily):
  @classmethod
  def Run(cls, controller):
    ws = controller.workspace
    v1 = ws.left
    v2 = ws.right
    category = ws.category
    b1 = v1.GetBindingsForCategory(category)
    if not b1:
      raise NoAnswerException(codelet_count=controller.steps_taken)
    ws.b1 = b1
    b2 = v2.GetBindingsForCategory(category)
    if not b2:
      raise NoAnswerException(codelet_count=controller.steps_taken)
    ws.b2 = b2
    ws.attribute_explanations = {}
    controller.AddCodelet(family=CF_ExplainValues, urgency=100)

class CF_ExplainValues(CodeletFamily):
  @staticmethod
  def CreateStructuralMappingFromExplanation(category, explanation):
    slippages = {}
    mappings = {}
    for right_attribute, val in explanation.items():
      left_attribute, mapping = val
      if left_attribute != right_attribute:
        slippages[right_attribute] = left_attribute
      mappings[right_attribute] = mapping
    return StructuralMapping(category=category,
                             bindings_mapping=frozenset(list(mappings.items())),
                             slippages=frozenset(list(slippages.items())))

  @classmethod
  def Run(cls, controller):
    ws = controller.workspace
    attribute_explanations = ws.attribute_explanations
    b2 = ws.b2
    b2_dict = b2.bindings
    unexplained_attributes = [x for x in list(b2_dict.keys()) if x not in attribute_explanations]
    one_attribute = random.choice(unexplained_attributes)
    logger.debug("Chose attribute %s for explanation.", one_attribute)
    attribute_value = b2_dict[one_attribute]
    logger.debug("Will love to explain this value: %s", str(attribute_value))
    # Pick an ordering of attributes (biased in some way... how, and how to implement bias?)
    # I wish there was a weighted choice in random :)
    b1 = ws.b1
    b1_dict = b1.bindings
    attributes_to_use = dict([(a, 1) for a in list(b1_dict.keys())])
    attributes_to_use[one_attribute] += 3
    for attribute_to_use in WeightedShuffle(list(attributes_to_use.items())):
      mapping = GetNaiveMapping(b1_dict[attribute_to_use], b2_dict[one_attribute])
      logger.debug("Used %s, saw mapping %s", attribute_to_use, str(mapping))
      if mapping:
        attribute_explanations[one_attribute] = (attribute_to_use, mapping)
        if ws.category.AreAttributesSufficientToBuild(list(attribute_explanations.keys())):
          # We have an explanation...
          full_mapping = CF_ExplainValues.CreateStructuralMappingFromExplanation(
              ws.category, attribute_explanations)
          raise AnswerFoundException(full_mapping, codelet_count=controller.steps_taken)
    controller.AddCodelet(family=CF_ExplainValues, urgency=100)


class SubspaceFindMapping(Subspace):
  class controller_class(Controller):
    class workspace_class:
      def __init__(self, left, right, category=None):
        self.left = left
        self.right = right
        self.category = category

  def QuickReconn(self):
    arguments = self.workspace_arguments
    if not arguments:
      arguments = dict()
    if 'category' in arguments and arguments['category']:
      mapping = arguments['category'].GetMapping(arguments['left'], arguments['right'])
    else:
      mapping = GetNaiveMapping(arguments['left'], arguments['right'])
    if mapping:
      return QuickReconnResults.AnswerFound(mapping)
    else:
      return QuickReconnResults.DeeperExplorationNeeded()

  def InitializeCoderack(self):
    self.controller.AddCodelet(family=CF_NumericCase, urgency=100)


class CF_FindAnchoredSimilarity(CodeletFamily):
  @classmethod
  def Run(cls, controller, left, right):
    if left.GetRelationTo(right):
      # Relation exists, bail out.
      return
    mapping = SubspaceFindMapping(controller,
                                  workspace_arguments=dict(left=left.object,
                                                           right=right.object,
                                                           category=None)).Run();
    if mapping:
      # TODO(# --- Jan 29, 2012): The relation should be formed with a probability dependent
      # on the distance between the nodes.
      relation = Relation(left, right, mapping)
      right.AddRelation(relation)
      left.AddRelation(relation)
      controller.ltm.AddEdgeBetweenContent(left.object, right.object, 'related')
      controller.ltm.AddEdgeBetweenContent(right.object, left.object, 'related')
      from farg.apps.seqsee.codelet_families.all import CF_FocusOn
      controller.AddCodelet(family=CF_FocusOn, urgency=100,
                            arguments_dict=dict(focusable=relation))
