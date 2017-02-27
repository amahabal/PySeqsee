from farg.core.stopping_conditions import StoppingConditions, RegisterStoppingCondition
class BongardStoppingConditions(StoppingConditions):
  pass

# EDIT-ME: This is a dummy condition. Add your own if needed.
@RegisterStoppingCondition(BongardStoppingConditions, condition_name="5_codelets_or_more")
def FiveCodeletsOrMore(controller):
  return controller.coderack.CodeletCount() >= 5

