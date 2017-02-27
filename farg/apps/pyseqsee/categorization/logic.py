from _collections import defaultdict
import ast
import traceback

from farg.apps.pyseqsee.objects import PSObject
from farg.apps.pyseqsee.utils import PSObjectFromStructure
from farg.core.ltm.storable import LTMNodeContent


class InsufficientAttributesException(Exception):
  """Raised when instance creation is attempted with insufficient attributes.

  This could happen if we try to create an instance of BasicSuccessorCategory,
  but we only specify the length.
  """
  pass


class InconsistentAttributesException(Exception):
  """Raised when instance creation is attempted with attributes that don't line up.

  This could happen if we try to create an instance of BasicSuccessorCategory,
  but we specify that it starts at 7, ands at 9, and has length 17.
  """
  pass


class UnknownValue(object):
  """Represents a currently unknown value for a variable."""
  pass


def Verify(item, prop):
  """Returns item if prop is true, None otherwise."""
  if item is None:
    return None
  if prop:
    return item
  return None


def ConditionalValue(cond, val):
  if cond:
    return val
  return UnknownValue()


def PrintEvalDict(eval_dict):
  for k, v in eval_dict.items():
    if k == '__builtins__':
      continue
    if isinstance(v, PSObject):
      print('\t%s = PSObject %s' % (k, v.Structure()))
    else:
      print('\t%s = %s' % (k, v))


class Rule(object):

  def __init__(self, *, target, expression, ctx):
    self.target = target
    self.expression = expression
    self.expression_vars = set(self.CalculateVars(ctx))

  def CalculateVars(self, ctx):
    tree = ast.parse(self.expression, mode='eval')
    for node in ast.walk(tree):
      if isinstance(node, ast.Name):
        if node.id not in ctx:
          yield (node.id)

  def GetVars(self):
    return self.expression_vars

  def AreAllExpressionVarsKnown(self, vars_dict):
    for v in self.expression_vars:
      if v not in vars_dict:
        return False
      if isinstance(vars_dict[v], UnknownValue):
        return False
    return True

  def IsTargetKnown(self, vars_dict):
    if self.target not in vars_dict:
      return False
    if isinstance(vars_dict[self.target], UnknownValue):
      return False
    return True

  def ApplyRule(self, vars_dict):
    # print("Applying: %s <-- %s" % (self.target, self.expression))
    if self.IsTargetKnown(vars_dict):
      # print("Target known, nothing to do.")
      # Nothing to do.
      return False
    if not self.AreAllExpressionVarsKnown(vars_dict):
      # print("Not all needed expressions known.")
      # Cannot apply.
      return False
    try:
      new_val = eval(self.expression, vars_dict)
    except Exception as e:
      # print("Exception! ", e)
      pass
    else:
      # print("Got new val: ", new_val)
      vars_dict[self.target] = new_val
      return not (isinstance(new_val, UnknownValue))

  def ApplyCheck(self, vars_dict):
    """Checks don't have targets.

    If all variables have values, the expression is evaluated.

    If all values are present, it is not acceptable to have an exception raised
    in the check.
    """
    if not self.AreAllExpressionVarsKnown(vars_dict):
      # The check does not appl.
      return True
    try:
      validity = eval(self.expression, vars_dict)
    except:
      return False
    return validity


class PSCategory(LTMNodeContent):
  """Base category for defining categories.

  Categories are defined "declaratively", meaning that we define the
  characteristics (such as attributes, relationships between parts, etc) as
  python code, in a way that allows easy reuse for both creating instances,
  checking membership, introspecting, and for creating relations.
  """

  #: Attributes are the "public" attributes. These are exposed in instance logic (which describes
  #: how something is an instance of a category. Contrast this with variables, which are a superset
  #: of attributes and can contain some internal stuff not exposed.
  #: Values for attributes should be proper PySeqsee objects (such as PSElement), since these are
  #: first class members of the workspace and can have thei own categories.
  _Attributes = set()

  #: Some categories may have attributes that are "hidden" by default but can be turned on later.
  #: As an instance, consider the category "even numbers". In many situations, we will want to
  #: do something with 'half' of this value---that is, an attribute of "18" as an instance of the
  #: category "Even" is that its half is 9---but we may not always want to automatically calculate
  #: the half. _TurnedOnAttributes explicitly list those attributes that are on.
  #: Currently, we do not optimize calculations by not calculating these---we just don't put them
  #: into the output.
  _TurnedOffAttributes = set()

  _RequiredAttributes = set()

  #: Rules describe how to calculate some variable given the values for others. When a rule is "fired",
  #: a value is calculated for the target. If this calculation is successful (that is, when there is
  #: no exception and the returned value is not UnknownValue, the value of the target variable is
  #: updated. A rule is only attempted when the target variables value is UnknownValue, and none of
  #: the variables mentioned on the RHS has an UnknownValue.
  #: A special class of rules is the guessers, which guess values for attributes given an instance
  #: whose membership we are evaluating.
  _Rules = []

  #: Checks are to ensure that the attributes and their values we have come up with are consistent
  #: with the category. Some category may require the length of its instances to be even, and this
  #: can be expressed as a check.
  _Checks = []

  #: Constructors take a subset of variables and can create an instance of the class using these.
  #: Constructors are tried in the order of their definition.
  _Constructors = {('_INSTANCE',): (lambda _INSTANCE: _INSTANCE)}

  #: Context refers to external variables that we need to pass in for evaluating the RHS of rules
  #: or evaluating checks.
  _Context = dict()

  _RelationCategories = ()

  def __init__(self):
    #: Variables are a superset of Attributes: they additionally contain internal, attribute-like
    #: things, that don't need to be made public. There are no constraints on the values for
    #: non-attribute variables.
    self._Variables = set()  # We will add to these.
    self._Variables.update(self._Attributes)
    #: Compiled rules are obtained from the string versions by parsing and seeking out variables.
    self._CompiledRules = []
    for rule in self._Rules:
      target, rest = rule.split(sep=':', maxsplit=1)
      rule_obj = Rule(
          target=target.strip(), expression=rest.lstrip(), ctx=self._Context)
      self._Variables.add(target.strip())
      self._Variables.update(x for x in rule_obj.GetVars())
      self._CompiledRules.append(rule_obj)

    #: Compiled checks. These are expressed as rules, but there is no target.
    self._CompiledChecks = []
    for rule in self._Checks:
      rule_obj = Rule(target=None, expression=rule.strip(), ctx=self._Context)
      self._Variables.update(x for x in rule_obj.GetVars())
      self._CompiledChecks.append(rule_obj)

    self.SanityCheck()

  def SanityCheck(self):
    # Make sure that every variable is either in attributes or context or starts with _.
    if not self._Constructors:
      raise Exception('No constructors defined.')
    for v in self._Variables:
      if v in self._Attributes:
        if v.startswith('_'):
          raise Exception('Attributes should not start with _')
      else:
        if v not in self._Context:
          if not v.startswith('_'):
            raise Exception(
                'Attribute %s neither in attributes nor in context, and does '
                'not start with _' % v)

  def CreateInstance(self, **kwargs):
    # Set values of missing  attributes to UnknownValue.
    for attr in self._Variables:
      if attr not in kwargs:
        kwargs[attr] = UnknownValue()
    # Add all external vals
    for k, v in self._Context.items():
      kwargs[k] = v
    self._RunInference(kwargs)
    if not self._CheckConsistency(kwargs):
      # PrintEvalDict(kwargs)
      raise InconsistentAttributesException()
    # Now we go through constructors, checking if we have all the necessary bits for any constructor
    # PrintEvalDict(kwargs)
    for args, constructor in self._Constructors.items():
      # print("Checking args: ", args)
      any_missing = False
      dict_to_pass_constructor = dict()
      for arg in args:
        if isinstance(kwargs[arg], UnknownValue):
          any_missing = True
          break
        dict_to_pass_constructor[arg] = kwargs[arg]
      if any_missing:
        continue
      return constructor(**dict_to_pass_constructor)
    raise InsufficientAttributesException()

  def Attributes(self):
    return self._Attributes

  def TurnOnAttribute(self, attribute):
    self._TurnedOffAttributes.discard(attribute)

  def TurnOffAttribute(self, attribute):
    self._TurnedOffAttributes.add(attribute)

  def IsInstance(self, item):
    eval_dict = dict()
    # Set values of all variables to None.
    for attr in self._Variables:
      eval_dict[attr] = UnknownValue()
    for k, v in self._Context.items():
      eval_dict[k] = v
    eval_dict['_INSTANCE'] = item
    self._RunInference(eval_dict)
    try:
      constructed = self.CreateInstance(**eval_dict)
    except Exception as e:
      # print("Exception during construction: ", e)
      # PrintEvalDict(eval_dict)
      # print(traceback.format_tb(e.__traceback__))
      return None
    else:
      if (constructed != item) and (constructed.Structure() != item.Structure()
                                   ):
        return None
      guessed_vals = dict()
      for attr in self._Attributes:
        if attr in self._TurnedOffAttributes:
          continue
        if not (isinstance(eval_dict[attr], UnknownValue)):
          guessed_vals[attr] = eval_dict[attr]
      return InstanceLogic(attributes=guessed_vals)

  def _RunInference(self, values_dict):
    any_new_known = False
    for rule in self._CompiledRules:
      if rule.ApplyRule(values_dict):
        any_new_known = True
    if any_new_known:
      self._RunInference(values_dict)

  def _CheckConsistency(self, values_dict):
    for attr in self._RequiredAttributes:
      if attr not in values_dict or values_dict[attr] is None or isinstance(
          values_dict[attr], UnknownValue):
        return False
    for rule in self._CompiledChecks:
      if not rule.ApplyCheck(values_dict):
        return False
    return True


class InstanceLogic(object):
  """Describes how an item is an instance of a category.

    TODO(amahabal): What about cases where an item can be seen as an instance of
    a category in a
    number of ways? When that happens, there are rich possibilities for creation
    of novel categories
    that we should not miss out on. Punting on this issue at the moment.
    One way to achieve this would be to add the method ReDescribeAs to
    categorizable, which will
    not use the stored logic; it will then look at the two logics and perhaps
    merge.
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

    That is, if other_logic has extra attributes, they are added here. If, for
    an existing attribute
    there are extra category annotations in other_logic, they are added on the
    annotation here, and
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
