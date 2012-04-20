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
from farg.core.exceptions import SuccessfulCompletion
from farg.core.ui.batch_ui import BatchUI
from farg.third_party import gflags
import sys

FLAGS = gflags.FLAGS

def HasAsPrefix(longer_list, shorter_list):
  return longer_list[:len(shorter_list)] == shorter_list

class SeqseeBatchUI(BatchUI):
  def RegisterQuestionHandlers(self):
    def HandleNextTermsQuestion(question, ui):
      workspace = ui.controller.workspace
      current_known_terms = list(x.object.magnitude for x in workspace.elements)
      total_known_terms = FLAGS.sequence + FLAGS.unrevealed_terms
      expected_total_terms = current_known_terms + list(question.terms)
      if len(expected_total_terms) > len(total_known_terms):
        if (HasAsPrefix(expected_total_terms, total_known_terms)):
          raise SuccessfulCompletion(codelet_count=ui.controller.steps_taken)
        else:
          return False
      else:
        return HasAsPrefix(total_known_terms, expected_total_terms)
    AreTheseTheNextTermsQuestion.Ask = HandleNextTermsQuestion
