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

  _flipmap_ = { 'succ': 'pred', 'pred': 'succ', 'same': 'same', 'flip': 'flip', 'noflip': 'noflip'}


  def FlippedVersion(self):
    return NumericMapping(NumericMapping._flipmap_[self.name], self.category)

class StructuralMapping(Mapping):
  def __init__(self, category, bindings_mapping, slippages, metonymy_mode,
               position_mapping=None, metonymy_mapping=None):
    #: A category, such as ascending, on which mapping is based.
    self.category = category
    #: A dictionary of attribute to a mapping: how is the value of each attribute transformed?
    self.bindings_mapping = bindings_mapping
    #: If an attribute comes from a different attribute, that information is here.
    #: Thus, if the new `start` is the successory of the old `end`, then there will be an entry
    #: start => end in the slippages dictionary, as well as a start => succ in the bindings_mapping
    #: dictionary.
    self.slippages = slippages
    #: Metonymy mode of each end of the mapping.
    self.metonymy_mode = metonymy_mode
    #: If position is relevant, how position changes.
    self.position_mapping = position_mapping
    #: If metonymy is relevant, how it changes.
    self.metonymy_mapping = metonymy_mapping
