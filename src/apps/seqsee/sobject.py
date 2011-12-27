"""Represents a group or a single number in a sequence.

.. warning:: This is an implementation of the SObject in Perl, but differs significantly in the
   ways described below.

   * The class hierarchy is different. Whereas previously I had a messed up SElement isa SAnchored
     isa SObject, now positioned stuff merely holds an SObject instance instead of inheriting.
   * With this, the responsibility of objects (now SElement and SGroup, both subclasses of
     SObject) is to maintain structure and structure related information (such as categories), and
     not positional or specific use information (such as metonyms).
"""

from farg.category import CategorizableMixin
from farg.exceptions import FargError, FargException, AnswerFoundException, NoAnswerException
from farg.ltm.storable import LTMMakeStorableMixin
from farg.codelet import Codelet, CodeletFamily
from farg.controller import Controller
import logging

logger = logging.getLogger(__name__)

class SObject(CategorizableMixin, LTMMakeStorableMixin):
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
  def Create(*items):
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

  def GetStorable(self):
    return self.Structure()

class SGroup(SObject):
  """A subclass of SObject representing things with an internal structure."""
  def __init__(self, underlying_mapping=None, items=[]):
    SObject.__init__(self, is_group=True)
    #: Underlying mapping on which object is based.
    self.underlying_mapping = underlying_mapping
    #: Items in the object
    self.items = items

  def DeepCopy(self):
    """Makes a copy of the group."""
    new_items = [x.DeepCopy() for x in self.items]
    new_object = SGroup(items=new_items,
                        underlying_mapping=self.underlying_mapping)
    # .. ToDo:: Copy categories as well.
    return new_object

  def Structure(self):
    """A tuple representations of the group."""
    return tuple(x.Structure() for x in self.items)

  def GetFringe(self):
    """Fringe for the group."""
    fringe = {}
    if self.underlying_mapping:
      fringe[self.underlying_mapping] = 1.0
    return fringe

class SElement(SObject):
  """A subclass of SObject, where there is a single element, which is a number."""
  def __init__(self, magnitude):
    SObject.__init__(self, is_group=False)
    #: An integer representing the number help by the SElement.
    self.magnitude = magnitude
    # .. ToDO:: (handle strength, primality, etc).
    # .. ToDo:: Copy categories as well.

  def DeepCopy(self):
    """Makes a copy."""
    # .. ToDo:: The copying business is likely indequate.
    return SElement(self.magnitude)

  def Structure(self):
    """The structure is the magnitude."""
    return self.magnitude

  def GetFringe(self):
    """Fringe for the element."""
    fringe = {'mag:%d' % self.magnitude: 1.0,
              'mag:%d' % (self.magnitude - 1): 0.8,
              'mag:%d' % (self.magnitude + 1): 0.8,
              }
    return fringe


class NonAdjacentGroupElementsException(FargException):
  pass

class SAnchored(LTMMakeStorableMixin):
  """An object with position information.
  
  .. warning:: This way of doing things differs from the way in Perl, where I was
    subclassing instead of just having an sobject as a member.
  """
  def __init__(self, sobj, items, start_pos, end_pos, is_sequence_element=False):
    #: The object which is anchored.
    self.object = sobj
    #: The items --- sub-anchored-objects --- that make up this object. Empty if this has no
    #: structure (i.e., it holds an SElement).
    self.items = items
    #: The start position. The first element in the workspace has position 0.
    self.start_pos = start_pos
    #: The end position. Note that this is the rightmost edge (unlike, say, iterators).
    #: For an element, left and right edges are identical.
    self.end_pos = end_pos
    #: All items in the workspace --- what used to be elements and groups in the Perl version ---
    #: are SAnchored objects now. This bit distinguishes elements that are elements in the
    #: sequence.
    self.is_sequence_element = is_sequence_element
    #: What metonym does this have? Metonym, if present, is a SObject.
    self.metonym = None
    #: Is the metonym active?
    self.is_metonym_active = False
    #: Relations.
    self.relations = set()

  def SetPosition(self, start_pos, end_pos):
    """Sets the end-point of the anchored object."""
    self.start_pos = start_pos
    self.end_pos = end_pos

  def Span(self):
    """Returns a 2-tuple with start and end points."""
    return (self.start_pos, self.end_pos)

  def Structure(self):
    """The structure of the contained object."""
    return self.object.Structure()

  def GetStorable(self):
    return self.Structure()

  @staticmethod
  def Create(*items):
    """Given a list of items, each a SAnchored, creates another SAnchored, provided that the
    items are contiguous. Raises a NonAdjacentGroupElementsException if they are non-adjacent."""
    if not items:
      raise FargError("Empty group creation attempted. An error at the moment")
    if len(items) == 1:
      if isinstance(items[0], SAnchored):
        return items[0]
      else:
        raise FargError("Attempt to SAnchored.Create() from non-anchored parts: %s" %
                        items[0].__repr__())

    # So there are multiple items...
    for item in items:
      if not isinstance(item, SAnchored):
        raise FargError("Attempt to SAnchored.Create() from non-anchored parts: %s" %
                        item.__repr__())
    # .. Note:: This can probably be speeded up and cleaned up.
    left_edge, right_edge = items[0].Span()
    for item in items[1:]:
      left, right = item.Span()
      if left != right_edge + 1:
        raise NonAdjacentGroupElementsException()
      right_edge = right
    return SAnchored(SObject.Create(list(x.object for x in items)), items,
                     left_edge, right_edge)


  def GetFringe(self):
    """Gets the fringe (needed for stream-related activities)."""
    fringe = { 'pos:%d' % self.start_pos: 0.6,
               'pos:%d' % self.end_pos: 0.6,
               'pos:%d' % (self.end_pos + 1): 0.3,
               'pos:%d' % (self.start_pos - 1): 0.3}
    for k, v in self.object.GetFringe().iteritems():
      fringe[k] = v
    return fringe

  def GetAffordances(self, controller):
    logging.debug('GetAffordances called for %s', self)
    return ()

  def GetSimilarityAffordances(self, other, other_fringe, my_fringe, controller):
    from apps.seqsee.get_mapping import CF_FindAnchoredSimilarity
    logging.debug('GetSimilarityAffordances called: [%s] and [%s] ', self, other)
    if not isinstance(other, SAnchored):
      return ()
    sorted_items = sorted((self, other), key=lambda x: x.start_pos)
    # So both are anchored, and have overlapping fringes. Time for subspaces!
    return [Codelet(CF_FindAnchoredSimilarity, controller, 100,
                    left=sorted_items[0], right=sorted_items[1])]

  def AddRelation(self, relation):
    self.relations.add(relation)

  def GetRelationTo(self, other):
    return [x for x in self.relations if (x.left == other or x.right == other)]

  def GetRightwardRelations(self):
    return [x for x in self.relations if x.left == self]

