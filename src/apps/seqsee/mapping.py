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


