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
"""Defines class for "Node" of an LTM."""

import math
import logging

kLogger = logging.getLogger("LTM_activations")

#: Maps raw activation (an integer) to real activation.
#: The values, in steps of 10, are as follows:
#: ['0.003', '0.018', '0.043', '0.093', # For 0, 10, 20, 30
#:  '0.220', '0.562', '0.811', '0.895', # For 40, 50, 60, 70
#:  '0.932', '0.952', '0.964']  # For 80, 90, 100
_RAW_ACTIVATION_TO_REAL_ACTIVATION = [
  0.4815 + 0.342 * math.atan2(12 * (0.01 * x - 0.5), 1)
  for x in range(2, 203)]

def _UnmangleTuple(value):
  out = []
  for k in value:
    if isinstance(k, tuple):
      out.append(_UnmangleTuple(k))
    elif isinstance(k, LTMNode):
      out.append(k.content)
    else:
      out.append(k)
  return tuple(out)

def Unmangle(content_dict):
  """Replaces values that are nodes with contents of those nodes."""
  for k, value in content_dict.items():
    if isinstance(value, tuple):
      content_dict[k] = _UnmangleTuple(value)
    elif isinstance(value, LTMNode):
      content_dict[k] = value.content


class LTMNode(object):
  """Represents a single concept stored in an LTM.

  Each node has a core --- content that is being remembered and connected to other concepts.

  This content must be derived from a subclass of LTMStorableMixin. The reason for this is to
  ensure proper creation. Creation of nodes occurs in two ways --- either via the
  constructor,. or by vivification during unpickling (that is, by the __init__ method or by
  __setstate__ method.

  An important number associated with a node is its activation (a number between 0 and 1 that
  represents how important that concept currently appears for the current problem).

  In practice, a substitute for this is stored: "raw activation" (which is a number
  between 0 and 100 which is converted by a sigmoid to a real activation). Raw activation makes
  things easier to calculate.

  The calculation of activation is lazy --- it is calculated when needed. Although the
  activation decays at every timestep, we do not bother updating it everytime, relying on a
  just-in-time calculation.
  """

  def __init__(self, content):
    """Initializes the node.

    Args:
      content: Create a node using content.

    .. note::

      Any change here must be reflected in the __getstate__ and __setstate__ methods.

    """
    self.content = content
    self.outgoing_edges = []
    #: An easy-to-update measure of activation. The real activation is a continuous function
    #: of this. Starts out at (and never falls below) 0.
    self._raw_activation = 0
    #: When was activation last updated? This is used so that activation can be calculated
    #: only when needed (not whenever decays happen, for instance!)
    self._time_of_activation_update = 0
    #: How many times has this node been seen as highly activated in problems?
    self.abundance = 1

  def __str__(self):
    return 'Node(%s)' % self.content.BriefLabel()

  def __getstate__(self):
    """Saves the class name of content and (mangled) __dict__, to be reconstructed later.

    Mangling consists of replacing any value with the node of which that value is the
    content.

    .. Note::

      Mangling cannot be done by the node. It is a graph-wide calculation. The mangling
      happens prior to calling dump() by the ltm.LTM pickler.

    This is needed since we wish to pass everything we are reviving through Create() of
    appropriate classes, and pickle has its own ideas of how to recreate. I wish to limit
    complexity to this class (rather than spreading to many), hence modifying how other
    classes get pickled is not an option.

    .. Note::

      Attributes whose name starts with an underscore are not dumped, and hence not passed to the
      cnstructor when vivifying later.

    Returns:
      4-tuple: class of content, dict of content, the outgoing edges, and abundance.
    """
    content = self.content
    attrib_dict = dict(kv for kv in content.__dict__.items() if not kv[0].startswith('_'))
    return (content.__class__, attrib_dict, self.outgoing_edges, self.abundance)

  def __setstate__(self, state):
    """This vivifies the object, using Create() and unmangling any values.

    That is, values that are nodes are replaced by their contents.

    Args:
      state: A 4-tuple (classname, arguments to pass to constructor of classname, outgoing edges,
                        abundance).
    """
    clsname, instance_dict, outgoing_edges, abundance = state
    Unmangle(instance_dict)
    self.content = clsname(**instance_dict)  # Fair use of ** magic. pylint: disable=W0142
    self.outgoing_edges = outgoing_edges
    self._raw_activation = 0
    self._time_of_activation_update = 0
    self.abundance = abundance

  def _ProcessDecays(self, current_time):
    """Process any pending decays. This helps keep activation calculation lazy."""
    timesteps_passed = current_time - self._time_of_activation_update
    if timesteps_passed > 0:
      self._raw_activation -= 0.1 * timesteps_passed
      if self._raw_activation < 0:
        self._raw_activation = 0
    self._time_of_activation_update = current_time

  def IncreaseActivationButDontSpread(self, amount, *, current_time):
    """Update activation by this amount (after processing any decays). No spreadings."""
    self._ProcessDecays(current_time)
    self._raw_activation += amount
    if self._raw_activation > 100:
      self._raw_activation = 100
    kLogger.debug("Raw activation of %s now %5.3f", self, self._raw_activation)

  def IncreaseActivation(self, amount, *, current_time):
    """Update activation by this amount (after processing any pending decays), and spread.

    Activation is spread an appropriate component to nearby nodes.

    Args:
      amount: Amount by which to increase. Will typically be a small integer.

    Keyword-only Args:
      current_time: Time when this method was called. Needed to process any pending decays.

    Returns:
      Activation at this time.

    .. todo::

      Should spread to depth 2. Not done correctly. Nor is the amount spread
      accurate.
    """
    self.IncreaseActivationButDontSpread(amount, #pylint:disable=E1123,C6010
                                         current_time=current_time)
    for edge in self.outgoing_edges:
      to_node = edge.to_node
      to_node.IncreaseActivationButDontSpread(0.25 * amount, current_time=current_time)
    return self.GetActivation(current_time)

  def GetRawActivation(self, current_time):
    """Get raw activation.

    Time is needed to calculate decay, if any, since the stored activation may be stale.

    Args:
      current_time: Number of codelets run thus far.

    Returns:
      Raw activation (number between 0 and 100). Real activation is a sigmoid of this.
    """
    self._ProcessDecays(current_time)
    return self._raw_activation

  def GetActivation(self, current_time):
    """Get activation. This is f(raw_activation), where f is a predefined mapping."""
    return _RAW_ACTIVATION_TO_REAL_ACTIVATION[int(self.GetRawActivation(current_time))]

  def GetOutgoingEdges(self):
    """Get outgoing edges from the node."""
    return self.outgoing_edges

  def GetOutgoingEdgesOfType(self, edge_type):
    """Get outgoing edges of particular type."""
    return (edge for edge in self.outgoing_edges if edge_type in edge.edge_type_set)

  def GetOutgoingEdgesOfTypeIsa(self):
    """Get outgoing edges of type 'isa'."""
    from farg.core.ltm.edge import LTMEdge
    return self.GetOutgoingEdgesOfType(LTMEdge.LTM_EDGE_TYPE_ISA)
