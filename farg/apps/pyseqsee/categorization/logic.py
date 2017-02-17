import ast
from farg.apps.pyseqsee.utils import PSObjectFromStructure
from _collections import defaultdict
from farg.core.ltm.storable import LTMNodeContent

class InsufficientAttributesException(Exception):
  """Raised when instance creation is attempted with insufficient attributes.

  This could happen if we try to create an instance of BasicSuccessorCategory, but we only specify
  the length.
  """
  pass

class InconsistentAttributesException(Exception):
  """Raised when instance creation is attempted with attributes that don't line up.

  This could happen if we try to create an instance of BasicSuccessorCategory, but we specify that
  it starts at 7, ands at 9, and has length 17.
  """
  pass

def Verify(item, prop):
  """Returns item if prop is true, None otherwise."""
  if item is None:
    return None
  if prop:
    return item
  return None

class Rule(object):
  def __init__(self, *, target, expression):
    self.target = target
    self.expression = expression
    self.vars = set(self.GetVars())

  def GetVars(self):
    tree = ast.parse(self.expression, mode='eval')
    for node in ast.walk(tree):
      if isinstance(node, ast.Name):
        yield(node.id)

class PyCategory(LTMNodeContent):

  _external_vals = dict()
  _guessers = []
  _rules = []

  def __init__(self):
    self._attributes = set()
    self._compiled_rules = []
    for rule in self._rules:
      target, rest = rule.split(sep=':', maxsplit=1)
      rule_obj = Rule(target=target.strip(), expression=rest.lstrip())
      self._attributes.add(target.strip())
      self._attributes.update(x for x in rule_obj.GetVars() if x not in self._external_vals)
      self._compiled_rules.append(rule_obj)

    self._compiled_guessers = defaultdict(list)
    for rule in self._guessers:
      target, rest = rule.split(sep=':', maxsplit=1)
      self._compiled_guessers[target.strip()].append(rest.lstrip())
    # print("Compiled guessers=", self._compiled_guessers)

  def CreateInstance(self, **kwargs):
    # Set values of missing  attributes to None.
    for attr in self._attributes:
      if attr not in kwargs:
        kwargs[attr] = None
    # Add all external vals
    for k, v in self._external_vals.items():
      kwargs[k] = v
    self._RunInference(kwargs)
    if not self._CheckConsistency(kwargs):
      raise InconsistentAttributesException()
    # Now we go through constructors, checking if we have all the necessary bits for any constructor
    for args, constructor in self._object_constructors.items():
      any_missing = False
      dict_to_pass_constructor = dict()
      for arg in args:
        if kwargs[arg] is None:
          any_missing = True
          break
        dict_to_pass_constructor[arg] = kwargs[arg]
      if any_missing:
        continue
      return constructor(**dict_to_pass_constructor)
    raise InsufficientAttributesException()

  def Attributes(self):
    return self._attributes

  def IsInstance(self, item):
    eval_dict = dict()
    # Set values of all attributes to None.
    for attr in self._attributes:
      eval_dict[attr] = None
    for k, v in self._external_vals.items():
      eval_dict[k] = v
    eval_dict['instance'] = item

    for target, expr_list in self._compiled_guessers.items():
      for expr in expr_list:
        try:
          val = eval(expr, eval_dict)
        except Exception as e:
          pass
        else:
          eval_dict[target] = val
          break
    self._RunInference(eval_dict)

    try:
      constructed = self.CreateInstance(**eval_dict)
    except Exception as e:
      # print("Exception during construction: ", e)
      # raise(e)
      return None
    else:
      if constructed.Structure() != item.Structure():
        return None
      guessed_vals = dict()
      for attr in self._attributes:
        if eval_dict[attr] is not None:
          guessed_vals[attr] = eval_dict[attr]
      return InstanceLogic(attributes=guessed_vals)

  def _RunInference(self, values_dict):
    any_new_known = False
    for rule in self._compiled_rules:
      if values_dict[rule.target] is None:
        if not any(values_dict[v] is None for v in rule.vars):
          try:
            evaled = eval(rule.expression, values_dict)
          except:
            pass
          else:
            values_dict[rule.target] = evaled
            any_new_known = True
    if any_new_known:
      self._RunInference(values_dict)

  def _CheckConsistency(self, values_dict):
    for rule in self._compiled_rules:
      if rule.target in values_dict and values_dict[rule.target] is not None:
        if not any(values_dict[v] is None for v in rule.vars):
          calculated_val =  eval(rule.expression, values_dict)
          if calculated_val.Structure() != values_dict[rule.target].Structure():
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
