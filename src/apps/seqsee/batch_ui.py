from tide.ui.batch_ui import BatchUI
from apps.seqsee.question import AreTheseTheNextTermsQuestion
from third_party import gflags
from farg.exceptions import FargException
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
          raise FargException("RunOutOfKnownFutureTerms")
        else:
          return False
      else:
        return HasAsPrefix(total_known_terms, expected_total_terms)
    AreTheseTheNextTermsQuestion.Ask = HandleNextTermsQuestion
