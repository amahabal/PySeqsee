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

import math

#: Maps raw activation (an integer) to real activation.
#: The values, in steps of 10, are as follows:
#: ['0.003', '0.018', '0.043', '0.093', # For 0, 10, 20, 30
#:  '0.220', '0.562', '0.811', '0.895', # For 40, 50, 60, 70
#:  '0.932', '0.952', '0.964']  # For 80, 90, 100
_RAW_ACTIVATION_TO_REAL_ACTIVATION = [
    0.4815 + 0.342 * math.atan2(12 * (0.01 * x - 0.5), 1)
    for x in range(2, 203)]

class LTMNode(object):
  """Represents a single concept stored in an LTM.

  Each node has a core --- content that is being remembered and connected to other concepts.
  
  This content must be derived from a subclass of LTMStorableMixin. The reason for this is to
  ensure proper creation. Creation of nodes occurs in two ways --- either via the
  constructor,. or by vivification during unpickling (that is, by the __init__ method or
  by __setstate__ method.
  
  There are two important numbers associated with a node. These are the activation (a number
  between 0 and 1 that represents how important that concept currently appears for the
  current problem), and its depth (an integer typically greater than 5 that represents the
  difficulty of raising or lowering activation --- deep concept's activation rises slowly and
  falls slowly.)
  
  In practice, two substitutes for these are stored: "raw activation" (which is a number
  between 0 and 100 which is converted by a sigmoid to a real activation), and the reciprocal
  of the depth (since that eases computation a bit). Raw activation makes things easier to
  calculate.
  
  The calculation of activation is lazy --- it is calculated when needed. Although the
  activation decays at every timestep, we do not bother updating it everytime, relying on a
  just in time calculation.
  """

  def __init__(self, content):
    """Initializes the node.
    
    .. note::
    
      Any change here must be reflected in the __getstate__ and __setstate__ methods.
      
    """
    self.content = content
    self.outgoing_edges = []
    #: An easy-to-update measure of activation. The real activation is a continuous function
    #: of this. Starts out at (and never falls below) 0.
    self._raw_activation = 0
    #: Depth of a node controls how quickly it accumulates or decays activation. The greater
    #: the depth, the slower this happens. Starts out at 5 and can go up from there.
    #: What is stored here is the reciprocal of depth, as that is what is needed in
    #: calculations.
    self.depth_reciprocal = 1.0 / 5
    #: When was activation last updated? This is used so that activation can be calculated
    #: only when needed (not whenever decays happen, for instance!)
    self._time_of_activation_update = 0

  def __str__(self):
    return 'Node(%s)' % self.content.BriefLabel()

  def __getstate__(self):
    """This saves the class name of content and (mangled) __dict__, to be reconstructed
    using Create().
    
    Mangling consists of replacing any value with the node of which that value is the content.
    
    .. Note::
    
      Mangling cannot be done by the node. It is a graph-wide calculation. The mangling
      happens prior to calling dump() by the ltm.LTM pickler.
    
    This is needed since we wish to pass everything we are reviving through Create() of 
    appropriate classes, and pickle has its own ideas of how to recreate. I wish to limit 
    complexity to this class (rather than spreading to many), hence modifying how other 
    classes get pickled is not an option.
    """
    content = self.content
    return (content.__class__, content.__dict__, self.outgoing_edges, self.depth_reciprocal)

  def __setstate__(self, state):
    """This vivifies the object, using Create() and unmangling any values: that is, values 
       that are nodes are replaced by their contents.
    """
    clsname, instance_dict, outgoing_edges, depth_reciprocal = state
    LTMNode._Unmangle(instance_dict)
    self.content = clsname(**instance_dict)  # Fair use of ** magic. pylint: disable=W0142
    self.outgoing_edges = outgoing_edges
    self._raw_activation = 0
    self._time_of_activation_update = 0
    self.depth_reciprocal = depth_reciprocal

  @staticmethod
  def _Unmangle(content_dict):
    """Replaces values that are nodes with contents of those nodes."""
    for k, value in content_dict.items():
      if isinstance(value, LTMNode):
        content_dict[k] = value.content

  def IncrementDepth(self):
    """Increment depth of node by 1."""
    depth = 1.0 / self.depth_reciprocal
    self.depth_reciprocal = 1.0 / (depth + 1)

  def _ProcessDecays(self, current_time):
    """Process any pending decays. This helps keep activation calculation lazy."""
    timesteps_passed = current_time - self._time_of_activation_update
    if timesteps_passed > 0:
      self._raw_activation -= 0.1 * timesteps_passed * self.depth_reciprocal
      if self._raw_activation < 0:
        self._raw_activation = 0
    self._time_of_activation_update = current_time

  def SpikeNonSpreading(self, amount, current_time):
    """Update activation by this amount (after processing any pending decays, but do not
       propagate further.)"""
    self._ProcessDecays(current_time)
    self._raw_activation += amount * self.depth_reciprocal
    if self._raw_activation > 100:
      self.IncrementDepth()
      self._raw_activation = 90

  def Spike(self, amount, current_time):
    """Update activation by this amount (after processing any pending decays), and also 
       spread an appropriate component to nearby nodes.
    
    .. todo:: Should spread to depth 2. Not done correctly. Nor is the amount spread accurate.
    """
    self.SpikeNonSpreading(amount, current_time)
    for edge in self.outgoing_edges:
      to_node = edge.to_node
      to_node.SpikeNonSpreading(0.25 * amount, current_time)
    return self.GetActivation(current_time)

  def GetRawActivation(self, current_time):
    """Get raw activation.
    
       Time is needed to calculate decay, if any, since the stored activation may be stale.
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
    return (edge for edge in self.outgoing_edges if edge.edge_type == edge_type)

  def GetOutgoingEdgesOfTypeRelated(self):
    """Get outgoing edges of type 'related'."""
    from farg.core.ltm.edge import LTMEdge
    return self.GetOutgoingEdgesOfType(LTMEdge.LTM_EDGE_TYPE_RELATED)

  def GetOutgoingEdgesOfTypeIsa(self):
    """Get outgoing edges of type 'isa'."""
    from farg.core.ltm.edge import LTMEdge
    return self.GetOutgoingEdgesOfType(LTMEdge.LTM_EDGE_TYPE_ISA)
