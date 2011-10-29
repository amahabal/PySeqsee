"""Represents a group or a single number in a sequence.

.. warning:: This is an implementation of the SObject in Perl. I will likely rework this once
  other pieces are in place.
"""

from farg.exceptions import FargError

class SObject(object):
  """Base class of objects --- groups or elements.
  
  This is an abstract class. SGroup and SElement are concrete subclasses.
  """
  def __init__(self, is_group=False):
    #: A number between 0 and 100.
    self.strength = 0
    #: Is this a group? Even SElements can occasionally act like groups.
    self.is_group = is_group
    #: What metonym does this have?
    self.metonym = None
    #: Is the metonym active?
    self.is_metonym_active = False
    #: What is this a metonym of (if anything)?
    self.is_a_metonym_of = None


  @staticmethod
  def Create(*items):
    if not items:
      return SGroup(items=[])
    if len(items) == 1:
      item = items[0]
      if isinstance(item, int):
        return SElement(item)
      elif isinstance(item, list):
        return SObject.Create(*item)
      elif isinstance(item, SObject):
        return item.DeepCopy()
      else:
        FargError("Bad argument to Create").Raise()
    # So there are multiple items...
    new_items = [SObject.Create(x) for x in items]
    return SGroup(items=new_items)

class SGroup(SObject):
  """A subclass of SObject representing things with an internal structure."""
  def __init__(self, underlying_mapping=None, items=[]):
    SObject.__init__(self, is_group=True)
    #: Underlying mapping on which object is based.
    self.underlying_mapping = underlying_mapping
    #: Items in the object
    self.items = items

  def DeepCopy(self):
    new_items = [SObject.Create(x) for x in self.items]
    new_object = SGroup(items=new_items,
                        underlying_mapping=self.underlying_mapping)
    # .. ToDo:: Copy categories as well.
    return new_object

class SElement(SObject):
  """A subclass of SObject, where there is a single element, which is a number."""
  def __init__(self, magnitude):
    SObject.__init__(self, is_group=False)
    self.magnitude = magnitude
    # .. ToDO:: (handle strength, primality, etc).
    # .. ToDo:: Copy categories as well.

  def DeepCopy(self):
    # .. ToDo:: The copying business is likely indequate.
    return SElement(self.magnitude)

class SAnchored(SObject):
  """An object with position information.
  
  .. warning:: This way of doing things differs from the way in Perl, where I was subclassing
    instead of just having an sobject as a member.
  """
  def __init__(self, sobj, start_pos, end_pos, is_sequence_element=False):
    #: The object which is anchored.
    self.object = sobj
    #: The start position. The first element in the workspace has position 0.
    self.start_pos = start_pos
    #: The end position. Note that this is the rightmost edge (unlike, say, iterators).
    #: For an element, left and right edges are identical.
    self.end_pos = end_pos
    #: All items in the workspace --- what used to be elements and groups in the Perl version ---
    #: are SAnchored objects now. This bit distinguishes elements that are elements in the
    #: sequence.
    self.is_sequence_element = is_sequence_element

  def SetPosition(self, start_pos, end_pos):
    self.start_pos = start_pos
    self.end_pos = end_pos

