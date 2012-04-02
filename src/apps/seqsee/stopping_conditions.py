stopping_conditions_dict = dict()

def RegisterStoppingCondition(*, condition_name):
  def decorator(func):
    stopping_conditions_dict[condition_name] = func
    return func
  return decorator

@RegisterStoppingCondition(condition_name="group_present")
def CheckGroupPresence(controller):
  return bool(controller.workspace.groups)
