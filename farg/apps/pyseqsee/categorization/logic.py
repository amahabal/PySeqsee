import ast
from farg.apps.pyseqsee.utils import PSObjectFromStructure

class AttributeInference(object):
  """A way to specify relationships between attributes.

  This can be used to infer values for missing attributes and to check consistency.
  """

  def __init__(self, rules_dict):
    """TODO: make it easier to pass this in, as a simple dict rather than list as here."""
    self.rules = rules_dict

  class Rule(object):
    def __init__(self, *, target, expression):
      self.target = target
      self.expression = expression
      self.vars = set(self.GetVars(expression))
      print(self.vars)

    def GetVars(self, expression):
      tree = ast.parse(expression)
      for node in ast.walk(tree):
        if isinstance(node, ast.Name):
          yield(node.id)

  def RunInference(self, values_dict):
    any_new_known = False
    for rule in self.rules:
      if rule.target not in values_dict or values_dict[rule.target] is None:
        if not any(v not in values_dict or values_dict[v] is None for v in rule.vars):
          values_dict[rule.target] = PSObjectFromStructure(eval(rule.expression, values_dict))
          any_new_known = True
    if any_new_known:
      self.RunInference(values_dict)

  def CheckConsistency(self, values_dict):
    for rule in self.rules:
      if rule.target in values_dict and values_dict[rule.target] is not None:
        if not any(v not in values_dict or values_dict[v] is None for v in rule.vars):
          calculated_val =  eval(rule.expression, values_dict)
          if calculated_val != values_dict[rule.target].Structure():
            return False
    return True


class InstanceLogic(object):
  """Describes how an item is an instance of a category.

    TODO(amahabal): What about cases where an item can be seen as an instance of a category in a
    number of ways? When that happens, there are rich possibilities for creation of novel categories
    that we should not miss out on. Punting on this issue at the moment.
    One way to achieve this would be to add the method ReDescribeAs to categorizable, which will
    not use the stored logic; it will then look at the two logics and perhaps merge.
  """

  def __init__(self, *, attributes=dict()):
    self._attributes = attributes

  def Attributes(self):
    return self._attributes

  def HasAttribute(self, *, attribute):
    return attribute in self._attributes

  def GetAttributeOrNone(self, *, attribute):
    if attribute in self._attributes:
      return self._attributes[attribute]
    return None

  def MergeLogic(self, other_logic):
    """Add attributes and annotation of attributes from other_logic.

    That is, if other_logic has extra attributes, they are added here. If, for an existing attribute
    there are extra category annotations in other_logic, they are added on the annotation here, and
    this is done recursively.
    """
    # Check that the structures of attributes are equal where both present, and merge categories
    # in.
    other_attribues = other_logic._attributes
    for k, v in self._attributes.items():
      if k in other_attribues:
        if v.Structure() != other_attribues[k].Structure():
          return

    for k, v in other_attribues.items():
      if k in self._attributes:
        self._attributes[k].MergeCategoriesFrom(v)
      else:
        self._attributes[k] = v
