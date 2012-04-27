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
from collections import defaultdict
from farg.core.subspace import Subspace, QuickReconnResults
from farg.core.codelet import CodeletFamily
from farg.core.util import UnweightedChoice, SelectWeightedByActivation
from farg.core.exceptions import NoAnswerException
from farg.apps.seqsee.mapping import Mapping
from farg.apps.seqsee.categories import SizeNCategory

"""Subspace to explore whether the group may be interlaced."""

class CF_FindMappingAtModulus(CodeletFamily):
  @classmethod
  def Run(cls, controller, modulus):
    # As a first iteration (improve this), we'll look at successive items at positions a + kd
    # trying to make sense of *known* relations between them.
    # a is the moduli, d is the "jump" and k is a variable.
    workspace = controller.workspace
    parent_workspace = controller.parent_controller.workspace
    a = modulus
    assert workspace.distance.UnitIsElements()
    d = workspace.distance.value + 1
    assert d > 0
    maximum_element_position = parent_workspace.num_elements - 1
    maximum_k = int((maximum_element_position - a) / d)
    if maximum_k <= 1:
      # Not enough elements to make a decision
      workspace.mappings_found[modulus] = "NotEnoughElements"
      return
    known_relations = list(cls.GetRelations(parent_workspace, a, d, maximum_k))
    if len(known_relations) < 2:
      workspace.mappings_found[modulus] = "NotEnoughRelations"
      return
    #: I will generalize relations to potentially contain multiple mappings.
    mapping_sets = [x.GetMappingSet() for x in known_relations]

    mapping_counts = defaultdict(int)
    for m in mapping_sets:
      for x in m:
        mapping_counts[x] = mapping_counts[x] + 1
    mapping_intersection = set([x for x in mapping_counts.keys()
                                if mapping_counts[x] == len(mapping_sets)])
    if mapping_intersection:
      workspace.mappings_found[modulus] = SelectWeightedByActivation(
          controller.parent_controller.ltm,
          mapping_intersection)
    else:
      workspace.mappings_found[modulus] = "NoConsistentMapping"
    return


  @classmethod
  def GetRelations(cls, parent_workspace, a, d, maximum_k):
    for leftward_element_position in range(a, a + d * maximum_k, d):
      rightward_element_position = leftward_element_position + d
      left_element = parent_workspace.elements[leftward_element_position]
      right_element = parent_workspace.elements[rightward_element_position]
      list_of_potential_relations = left_element.GetRelationTo(right_element)
      if list_of_potential_relations:
        yield list_of_potential_relations[0]

class CF_IsThisAnInterlacedSequence(CodeletFamily):
  @classmethod
  def Run(cls, controller):
    # We reach here when all moduli have been looked at.
    # If all of them are mappings, we will try to impose this view of the sequence on it.
    if not cls.AllAreMapping(controller):
      raise NoAnswerException(codelet_count=controller.steps_taken)
    cls.CreateGroupings(controller)
    raise NoAnswerException(codelet_count=controller.steps_taken)

  @classmethod
  def AllAreMapping(cls, controller):
    for potential_mapping in controller.workspace.mappings_found.values():
      if not isinstance(potential_mapping, Mapping):
        return False
    return True

  @classmethod
  def CreateGroupings(cls, controller):
    from farg.apps.seqsee.anchored import SAnchored
    from farg.apps.seqsee.sobject import SGroup
    from farg.core.exceptions import ConflictingGroupException
    workspace = controller.workspace
    parent_workspace = controller.parent_controller.workspace
    d = workspace.distance.value + 1
    number_of_groups_possible = int(parent_workspace.num_elements / d)
    size_n_category = SizeNCategory(size=d)
    for k in range(number_of_groups_possible):
      items = [parent_workspace.elements[x] for x in range(k * d, (k + 1) * d)]
      sobj = SGroup(items=[x.object for x in items])
      group = SAnchored(sobj, items, k * d, (k + 1) * d - 1)
      group.object.DescribeAs(size_n_category)
      try:
        parent_workspace.InsertGroup(group)
      except ConflictingGroupException:
        # TODO(# --- Apr 22, 2012): add an appropriate codelet in top workspace.
        pass

class CF_LookForUndiscoveredMappings(CodeletFamily):
  """Looks for mappings for things for which we don't have mappings yet."""
  @classmethod
  def Run(cls, controller):
    missing_positions = CF_LookForUndiscoveredMappings.FindMissingMapping(controller)
    if not missing_positions:  # All have been found!
      controller.AddCodelet(family=CF_IsThisAnInterlacedSequence, urgency=100)
    else:
      modulus = UnweightedChoice(missing_positions)
      controller.AddCodelet(family=CF_FindMappingAtModulus, urgency=50,
                            arguments_dict=dict(modulus=modulus))

  @classmethod
  def FindMissingMapping(cls, controller):
    """Returns a set of missing mapping positions."""
    workspace = controller.workspace
    expected_mapping_positions = set(range(workspace.distance.value + 1))
    mappings_found = set(workspace.mappings_found.keys())
    return expected_mapping_positions - mappings_found

class SubspaceIsThisInterlaced(Subspace):
  from farg.core.controller import Controller
  class controller_class(Controller):

    routine_codelets_to_add = ((CF_LookForUndiscoveredMappings, 30, 0.3),)

    class workspace_class:
      def __init__(self, distance):
        self.distance = distance
        # Stores mappings found for various moduli. That is, if distance is "2 elements",
        # there are three interlaced sequences to deal with. This can store, in that case,
        # upto three mappings, with keys 0, 1 and 2.
        self.mappings_found = dict()

  def QuickReconn(self):
    if self.workspace_arguments['distance'].unit == 'Groups':
      # This has not yet been done.
      return QuickReconnResults.NoAnswerCanBeFound()
    else:
      return QuickReconnResults.DeeperExplorationNeeded()

  def InitializeCoderack(self):
    self.controller.AddCodelet(family=CF_LookForUndiscoveredMappings, urgency=100)


