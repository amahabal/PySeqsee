How to ask the user a question
==================================

You may need to interact with the user in the GUI mode (or even, during testing,
with a *simulated* user --- Seqsee, for instance, is really a conversation, and
"asks questions" even during testing).

Any question is an instance of a subclass of Question in 'farg.core.question.question'.
An example is 'AreTheseTheNextTermsQuestion' in Seqsee.

To Ask The Question
---------------------

If 'question' is an instance of the subclass of Question, you can ask it thus::

  controller.ui.AskQuestion(question)

What this does depends on the question handlers that have been installed in the
UI. The GUI and the Batch UI will probably have different versions. The skeleton
app generator creates two files --- batch_ui.py and gui/gui.py --- where you may
add a RegisterQuestionHandlers method. How it works is a bit hacky: for each class
of question it needs to handle, say, 'FooQuestion', it defines a function and
inserts it into the class::

  class BatchUI:
    def RegisterQuestionHandlers(self):
      def HandleFooQuestion(question, ui):
        ...
      FooQuestion.Ask = HandleFooQuestion

This allows inheritance. For the GUI case, a handler for BooleanQuestion is in
the core and does not need to be explicitly defined (although you would need to
define one for the BatchUI).


