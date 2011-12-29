"""A way to specify how two entities are related."""

class Mapping(object):
  pass

class NumericMapping(Mapping):
  def __init__(self, name, category):
    #: A string such as "succ" or "same". There are only 5 distinct values used in the Perl
    #: version: *succ*, *pred*, *same*, *flip*, and *noflip*.
    self.name = name
    #: A category (such as "Prime") on which this mapping is based.
    self.category = category

  _flipmap_ = { 'succ': 'pred', 'pred': 'succ', 'same': 'same', 'flip': 'flip',
                'noflip': 'noflip'}


  def FlippedVersion(self):
    return NumericMapping(NumericMapping._flipmap_[self.name], self.category)

  def Apply(self, item):
    return self.category.ApplyMapping(self, item)

  @classmethod
  def DifferenceString(cls, old_val, new_val):
    diff = new_val - old_val
    if diff == 1:
      return "succ"
    elif diff == 0:
      return "same"
    elif diff == -1:
      return "pred"
    else:
      return None


class StructuralMapping(Mapping):
  def __init__(self, category, bindings_mapping, slippages=None):
    #: A category, such as ascending, on which mapping is based.
    self.category = category
    #: A dictionary of attribute to a mapping: how is the value of each attribute 
    #: transformed?
    self.bindings_mapping = bindings_mapping
    #: If an attribute comes from a different attribute, that information is here.
    #: Thus, if the new `start` is the successory of the old `end`, then there will be an 
    #: entry start => end in the slippages dictionary, as well as a start => succ in the
    #: bindings_mapping dictionary.
    self.slippages = slippages

  def Apply(self, item):
    bindings = item.GetBindingsForCategory(self.category)
    new_bindings = {}
    for attribute, v in self.bindings_mapping.iteritems():
      new_binding_for_attribute = v.Apply(bindings.GetBindingsForAttribute(attribute))
      new_bindings[attribute] = new_binding_for_attribute
    return self.category.Create(new_bindings)

  def IsPairConsistent(self, item1, item2):
    """Is the pair of items consistent with this mapping?
    
    .. ToDo:: This is a cop-out, currently; when extending Seqsee, I should revisit this.
    """
    return self.Apply(item1).Structure() == item2.Structure()
