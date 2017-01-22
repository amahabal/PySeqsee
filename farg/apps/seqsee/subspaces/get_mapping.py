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

from farg.apps.seqsee.mapping import NumericMapping, StructuralMapping, FindMapping
from farg.apps.seqsee.relation import Relation
from farg.core.codelet import CodeletFamily
from farg.core.controller import Controller
from farg.core.exceptions import AnswerFoundException, NoAnswerException
from farg.core.subspace import QuickReconnResults, Subspace
from farg.core.util import WeightedShuffle, WeightedChoice, Toss
import logging
import random

from farg.apps.seqsee.sobject import SGroup
import sys
import farg_flags

# TODO(#53 --- Dec 29, 2011): Needs big fat documentation.

logger = logging.getLogger(__name__)

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
    b2 = ws.binding2
    b2_dict = b2.bindings
    unexplained_attributes = [x for x in list(b2_dict.keys())
                              if x not in attribute_explanations]
    one_attribute = random.choice(unexplained_attributes)
    logger.debug("Chose attribute %s for explanation.", one_attribute)
    attribute_value = b2_dict[one_attribute]
    logger.debug("Will love to explain this value: %s", str(attribute_value))
    # Pick an ordering of attributes (biased in some way... how, and how to implement bias?)
    # I wish there was a weighted choice in random :)
    b1 = ws.binding1
    b1_dict = b1.bindings
    attributes_to_use = dict([(a, 1) for a in list(b1_dict.keys())])
    attributes_to_use[one_attribute] += 3
    for attribute_to_use in WeightedShuffle(list(attributes_to_use.items())):
      mapping = FindMapping(b1_dict[attribute_to_use], b2_dict[one_attribute],
                            controller=controller, seqsee_ltm=ws.seqsee_ltm)
      if mapping:
        attribute_explanations[one_attribute] = (attribute_to_use, mapping)
        if ws.category.AreAttributesSufficientToBuild(list(attribute_explanations.keys())):
          # We have an explanation...
          full_mapping = CF_ExplainValues.CreateStructuralMappingFromExplanation(
              ws.category, attribute_explanations)
          raise AnswerFoundException(full_mapping, codelet_count=controller.steps_taken)
    controller.AddCodelet(family=CF_ExplainValues, urgency=100)


class SubspaceFindBindingMapping(Subspace):
  """
  Subspace to find mapping based on a pair of bindings.
  """
  class controller_class(Controller):
    class workspace_class:
      """
      Workspace for finding a mapping based on a pair of bindings.
      """
      def __init__(self, *, category, binding1, binding2, seqsee_ltm):
        """
        Initialize workspace.

        @param category: Category on which bindings are based.
        @param binding1: The binding for first object.
        @param binding2: The binding for the second object.
        @param seqsee_ltm: Seqsee's main LTM, needed to compare relative activations of
            various entities.
        """
        self.category = category
        self.binding1 = binding1
        self.binding2 = binding2
        self.seqsee_ltm = seqsee_ltm
        self.attribute_explanations = dict()

  def InitializeCoderack(self):
    self.controller.AddCodelet(family=CF_ExplainValues, urgency=100)

class CF_FindAnchoredSimilarity(CodeletFamily):
  @classmethod
  def Run(cls, controller, left, right, seqsee_ltm):
    if left.GetRelationTo(right):
      # Relation exists, possibly bail out.
      if Toss(farg_flags.FargFlags.double_mapping_resistance):
        return
    mapping = FindMapping(left.object, right.object, controller=controller,
                          seqsee_ltm=seqsee_ltm)
    if mapping:
      # TODO(# --- Jan 29, 2012): The relation should be formed with a probability dependent
      # on the distance between the nodes.
      relations = left.GetRelationTo(right)
      if relations:
        relation = relations[0]
        if mapping not in relation.mapping_set:
          # New relation, yay!
          relation.mapping_set.add(mapping)
      else:
        relation = Relation(left, right, mapping_set={mapping})
        right.AddRelation(relation)
        left.AddRelation(relation)
      controller.ltm.AddEdge(left.object, right.object)
      controller.ltm.AddEdge(right.object, left.object)
      from farg.apps.seqsee.codelet_families.all import CF_FocusOn
      controller.AddCodelet(family=CF_FocusOn, urgency=100,
                            arguments_dict=dict(focusable=relation))
