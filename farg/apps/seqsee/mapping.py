# Copyright (C) 2011, 2012  Abhijit Mahabal
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>

"""A way to specify how two entities are related."""

from farg.core.ltm.storable import LTMStorableMixin
from farg.core.meta import MemoizedConstructor

class Mapping(LTMStorableMixin, metaclass=MemoizedConstructor):
  pass

class NumericMapping(Mapping):
  def __init__(self, name, category):
    #: A string such as "succ" or "same". There are only 5 distinct values used in the Perl
    #: version: *succ*, *pred*, *same*, *flip*, and *noflip*.
    self.name = name
    #: A category (such as "Prime") on which this mapping is based.
    self.category = category

  def __str__(self):
    return 'NumericMapping(%s %s)' % (self.category.BriefLabel(), self.name)

  def BriefLabel(self):
    return '{%s} %s' % (self.category.BriefLabel(), self.name)

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

  def IsPairConsistent(self, item1, item2):
    return self.Apply(item1).Structure() == item2.Structure()

  def LTMDependentContent(self):
    return (self.category,)

class StructuralMapping(Mapping):
  def __init__(self, category, bindings_mapping, slippages=None,
               no_flipped_version=None,
               flipped_version=None):
    #: A category, such as ascending, on which mapping is based.
    self.category = category
    #: A dictionary of attribute to a mapping: how is the value of each attribute 
    #: transformed?
    assert isinstance(bindings_mapping, frozenset)
    self.bindings_mapping = bindings_mapping
    #: If an attribute comes from a different attribute, that information is here.
    #: Thus, if the new `start` is the successor of the old `end`, then there will be an 
    #: entry start => end in the slippages dictionary, as well as a start => succ in the
    #: bindings_mapping dictionary.
    assert not(slippages) or isinstance(slippages, frozenset)
    self.slippages = slippages

    self.no_flipped_version = False
    self.flipped_version = None

  def BriefLabel(self):
    return '[%s]' % self.category.BriefLabel()

  def Apply(self, item):
    bindings = item.DescribeAs(self.category)
    if not bindings:
      return
    new_bindings = {}
    for attribute, v in self.bindings_mapping:
      new_binding_for_attribute = v.Apply(bindings.GetBindingsForAttribute(attribute))
      new_bindings[attribute] = new_binding_for_attribute
    return self.category.Create(new_bindings)

  def IsPairConsistent(self, item1, item2):
    """Is the pair of items consistent with this mapping?
    
    .. ToDo:: This is a cop-out, currently; when extending Seqsee, I should revisit this.
    """
    return self.Apply(item1).Structure() == item2.Structure()

  def FlippedVersion(self):
    if self.no_flipped_version:
      return None
    if self.flipped_version:
      return self.flipped_version
    flipped = self.GetFlippedVersion()
    if flipped:
      self.flipped_version = flipped
      return flipped
    else:
      self.no_flipped_version = True
      return None

  def GetFlippedVersion(self):
    new_bindings_mappings = dict()
    for attribute, mapping in self.bindings_mapping:
      flipped = mapping.FlippedVersion()
      if not flipped:
        return None
      new_bindings_mappings[attribute] = flipped
    if not self.slippages:
      return StructuralMapping(self.category, frozenset(list(new_bindings_mappings.items())))
    # TODO(# --- Feb 16, 2012): Flip items with slippages when possible.
    return None

  def LTMDependentContent(self):
    return (self.category,)
