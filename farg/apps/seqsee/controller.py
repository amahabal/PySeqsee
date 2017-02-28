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

import logging
import sys

from farg.apps.seqsee.codelet_families.all import CF_RemoveSpuriousRelations
from farg.apps.seqsee.codelet_families.read_from_ws import CF_ReadFromWS
from farg.apps.seqsee.workspace import Workspace
from farg.core.controller import Controller
from farg.core.ltm.edge import LTMEdge
from farg.core.ltm.manager import LTMManager
import farg.flags as farg_flags
kLTMName = "seqsee.main"


def InitializeSeqseeLTM(ltm):
  """Called if ltm was empty (had no nodes)."""
  logging.info("Initializing Seqsee LTM")
  from farg.apps.seqsee.sobject import SElement
  # Creates nodes for elements corresponding to the integers 1 through 10.
  elements = [SElement(magnitude) for magnitude in range(1, 11)]
  for element in elements:
    ltm.GetNode(content=element)
  for idx, element in enumerate(elements[:-1]):
    ltm.AddEdge(element, elements[idx + 1])
    ltm.AddEdge(elements[idx + 1], element)
  from farg.apps.seqsee.categories import Prime, Squares, TriangularNumbers
  for prime_number in Prime.number_list[:10]:
    ltm.AddEdge(
        SElement(prime_number),
        Prime(),
        edge_type_set={LTMEdge.LTM_EDGE_TYPE_ISA})
  for square in Squares.number_list[:10]:
    ltm.AddEdge(
        SElement(square), Squares(), edge_type_set={LTMEdge.LTM_EDGE_TYPE_ISA})
  for triangular in TriangularNumbers.number_list[:10]:
    ltm.AddEdge(
        SElement(triangular),
        TriangularNumbers(),
        edge_type_set={LTMEdge.LTM_EDGE_TYPE_ISA})


LTMManager.RegisterInitializer(kLTMName, InitializeSeqseeLTM)


class SeqseeController(Controller):
  routine_codelets_to_add = ((CF_ReadFromWS, 30, 0.3),
                             (CF_RemoveSpuriousRelations, 30, 0.1))
  workspace_class = Workspace
  ltm_name = kLTMName

  def __init__(self, **args):
    logging.info("Initializing Seqsee controller")
    Controller.__init__(self, **args)
    self.workspace.InsertElements(farg_flags.FargFlags.sequence)
    self.unrevealed_terms = farg_flags.FargFlags.unrevealed_terms
