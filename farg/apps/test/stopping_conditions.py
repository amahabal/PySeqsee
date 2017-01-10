from farg.core.stopping_conditions import StoppingConditions, RegisterStoppingCondition

class TestStoppingConditions(StoppingConditions):
  pass

# EDIT-ME: This is a dummy condition. Add your own if needed.
@RegisterStoppingCondition(TestStoppingConditions, condition_name="5_codelets_or_more")
def FiveCodeletsOrMore(controller):
  return controller.coderack.CodeletCount() >= 5

