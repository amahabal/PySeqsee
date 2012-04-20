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

"""Represents a group or a single number in a sequence.

.. warning:: This is an implementation of the SObject in Perl, but differs significantly in
     the ways described below.

   * The class hierarchy is different. Whereas previously I had a messed up SElement isa
     SAnchored isa SObject, now positioned stuff merely holds an SObject instance instead of
     inheriting.
   * With this, the responsibility of objects (now SElement and SGroup, both subclasses of
     SObject) is to maintain structure and structure related information (such as
     categories), and not positional or specific use information (such as metonyms).
"""

from farg.core.categorization.categorizable import CategorizableMixin
from farg.core.exceptions import FargError
from farg.core.ltm.storable import LTMStorableMixin
from farg.core.meta import MemoizedConstructor
from farg.core.util import Squash
import logging

logger = logging.getLogger(__name__)

class LTMStorableSObject(LTMStorableMixin, metaclass=MemoizedConstructor):
  def __init__(self, structure):
    self.structure = structure

  def BriefLabel(self):
    return 'Obj:%s' % str(self.structure)

class SObject(CategorizableMixin, LTMStorableMixin):
  """Base class of objects --- groups or elements.
  
     This is an abstract class. SGroup and SElement are concrete subclasses.
  """
  def __init__(self, is_group=False):
    CategorizableMixin.__init__(self)
    #: A number between 0 and 100.
    self.strength = 0
    #: Is this a group? Even SElements can occasionally act like groups.
    self.is_group = is_group

  @staticmethod
  def Create(*items):  # pylint: disable=W0142
    """Creates an SObject given the items, which can be integers, lists, or other SObjects.
       * An integer is converted to an SElement.
       * Create([x, y, z]) is equivalent to Create(x, y, z)
       * Create(x, y, z) forms an SGroup made up of Create(x), Create(y) and Create(z)
       * Create(an Sobject) results in a DeepCopy of the SObject
    """
    if not items:
      raise FargError("Empty group creation attempted. An error at the moment")
    if len(items) == 1:
      item = items[0]
      if isinstance(item, int):
        return SElement(item)
      elif isinstance(item, list):
        return SObject.Create(*item)
      elif isinstance(item, tuple):
        return SObject.Create(*item)
      elif isinstance(item, SObject):
        return item.DeepCopy()
      else:
        raise FargError("Bad argument to Create: %s" % item.__repr__())
    # So there are multiple items...
    new_items = [SObject.Create(x) for x in items]
    return SGroup(items=new_items)

  def GetLTMStorableContent(self):
    # TODO(#24 --- Dec 28, 2011): Document (in LTM?) what GetStorable means.
    structure = self.Structure()
    return LTMStorableSObject(structure=structure)

  def Structure(self):  # pylint: disable=R0201
    """Should be overridden by subclasses to return an int or tuple representing the
       structure.
    """
    raise FargError("Structure should have been overridden.")

  def GetFringeFromLTM(self, controller):
    """Fringe for the element (now based off the LTM)."""
    # TODO(# --- Dec 30, 2011): Need codelets to add LTM edges where they are missing.
    my_node = controller.ltm.GetNodeForContent(self)
    my_node.Spike(50, controller.steps_taken)
    fringe = dict()
    fringe[my_node] = 1.0
    outgoing_related_edges = my_node.GetOutgoingEdgesOfTypeRelated()
    for edge in outgoing_related_edges:
      # TODO(# --- Dec 30, 2011): Edges should have strength, and it should influence this.
      fringe[edge.to_node] = 0.8
    return fringe


class SGroup(SObject):
  """A subclass of SObject representing things with an internal structure."""
  def __init__(self, underlying_mapping=None, items=None):
    SObject.__init__(self, is_group=True)
    #: Underlying mapping on which object is based.
    self.underlying_mapping = underlying_mapping
    #: Items in the object
    if not items:
      items = []
    self.items = items

  def DeepCopy(self):
    """Makes a copy of the group."""
    # TODO(#25 --- Dec 28, 2011): Should copy categories, too. Perhaps a method in
    # CategorizableMixin (CopyCategoriesFromCopy?). Also fix SElements below.
    new_items = [x.DeepCopy() for x in self.items]
    new_object = SGroup(items=new_items,
                        underlying_mapping=self.underlying_mapping)
    # .. ToDo:: Copy categories as well.
    return new_object

  def Structure(self):
    """A tuple representations of the group."""
    return tuple(x.Structure() for x in self.items)

  def GetFringe(self, controller):
    """Fringe for the group."""
    # TODO(#27 --- Dec 28, 2011): The categories are also a relevant part of the fringe.
    fringe = dict()
    if self.underlying_mapping:
      fringe[self.underlying_mapping] = 1.0
    for category, _bindings in self.categories.items():
      # QUALITY TODO(Feb 10, 2012): Activation in the LTM matters.
      fringe[category] = 0.8
    fringe.update(self.GetFringeFromLTM(controller))
    return fringe

  def Length(self):
    return sum(x.Length() for x in self.items)

  def FlattenedMagnitudes(self):
    flattened = []
    for part in self.items:
      flattened.extend(part.FlattenedMagnitudes())
    return flattened

  def CalculateStrength(self, controller=None):
    """The strength of a group is made up of a few components, including the strength of
       its parts and the strength of the underlying_mapping.
    """
    strength = sum(x.CalculateStrength(controller) for x in self.items)
    if controller and controller.ltm:
      if self.underlying_mapping:
        node = controller.ltm.GetNodeForContent(self.underlying_mapping)
        activation = node.GetActivation(controller.steps_taken)
        strength += 30 * activation
    return Squash(strength, 100)

class SElement(SObject):
  """A subclass of SObject, where there is a single element, which is a number."""
  def __init__(self, magnitude):
    SObject.__init__(self, is_group=False)
    #: An integer representing the number help by the SElement.
    self.magnitude = magnitude
    # .. ToDO:: (handle strength, primality, etc).
    # .. ToDo:: Copy categories as well.
    self.underlying_mapping = None

  def DeepCopy(self):
    """Makes a copy."""
    # .. ToDo:: The copying business is likely indequate.
    return SElement(self.magnitude)

  def Structure(self):
    """The structure is the magnitude."""
    return self.magnitude

  def GetFringe(self, controller):
    """Fringe for the element (now based off the LTM)."""
    fringe = dict()
    for category, _bindings in self.categories.items():
      # QUALITY TODO(Feb 10, 2012): Activation in the LTM matters.
      fringe[category] = 0.8
    fringe.update(self.GetFringeFromLTM(controller))
    return fringe

  def Length(self):
    return 1

  def FlattenedMagnitudes(self):
    return (self.magnitude,)

  def CalculateStrength(self, controller=None):
    # QUALITY TODO(Feb 18, 2012): WHat should "strength" mean? Should elements that have been
    # accounted for have a different strength?
    return 16.8067226891 # i.e., Squash(20, 100)
