from farg.codelet import CodeletFamily
from farg.subspace import Subspace
from farg.exceptions import NoAnswerException, AnswerFoundException
from apps.seqsee.question import AreTheseTheNextTermsQuestion

class CF_InitialEvaluation(CodeletFamily):
  @classmethod
  def Run(cls, controller):
    # For now, I'll require the basis of extension to be flush left.
    # QUALITY TODO(Feb 20, 2012): This can be improved vastly.
    if controller.workspace.basis_of_extension.start_pos != 0:
      raise NoAnswerException()
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
      workspace.seqsee_ws.InsertElements(*unknown_terms)
      raise AnswerFoundException(True)

class SubspaceGoBeyondKnown(Subspace):
  from tide.controller import Controller
  class controller_class(Controller):
    class workspace_class:
      def __init__(self, basis_of_extension, suggested_terms):
        self.basis_of_extension = basis_of_extension
        self.suggested_terms = suggested_terms

  @staticmethod
  def QuickReconn(**arguments):
    pass

  def InitializeCoderack(self):
    self.controller.AddCodelet(family=CF_InitialEvaluation, urgency=100)

