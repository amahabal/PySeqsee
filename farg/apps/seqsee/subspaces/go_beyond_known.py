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

from farg.apps.seqsee.question import AreTheseTheNextTermsQuestion
from farg.core.codelet import CodeletFamily
from farg.core.exceptions import NoAnswerException, AnswerFoundException
from farg.core.subspace import Subspace

class CF_InitialEvaluation(CodeletFamily):
  @classmethod
  def Run(cls, controller):
    # For now, I'll require the basis of extension to be flush left.
    # QUALITY TODO(Feb 20, 2012): This can be improved vastly.
    if controller.workspace.basis_of_extension.start_pos != 0:
      raise NoAnswerException(codelet_count=controller.steps_taken)
    # So we'll pop the question!
    my_ws = controller.workspace
    seqsee_ws = controller.parent_controller.workspace
    my_ws.seqsee_ws = seqsee_ws
    number_of_terms_already_known = (len(seqsee_ws.elements) -
                                     my_ws.basis_of_extension.end_pos - 1)
    my_ws.unknown_terms = my_ws.suggested_terms[number_of_terms_already_known:]
    controller.AddCodelet(family=CF_AskQuestion, urgency=100)

class CF_AskQuestion(CodeletFamily):
  @classmethod
  def Run(cls, controller):
    workspace = controller.workspace
    question = AreTheseTheNextTermsQuestion(workspace.unknown_terms)
    if controller.ui.AskQuestion(question):
      unknown_terms = workspace.unknown_terms
      workspace.seqsee_ws.InsertElements(unknown_terms)
      raise AnswerFoundException(True, codelet_count=controller.steps_taken)

class SubspaceGoBeyondKnown(Subspace):
  from farg.core.controller import Controller
  class controller_class(Controller):
    class workspace_class:
      def __init__(self, basis_of_extension, suggested_terms):
        self.basis_of_extension = basis_of_extension
        self.suggested_terms = suggested_terms

  def InitializeCoderack(self):
    self.controller.AddCodelet(family=CF_InitialEvaluation, urgency=100)

