"""Workspace. Modeled after the workspace in the Perl version.

.. warning:: No attempt to optimize is being made. Later, with profiling, we can speed things up.
"""

from apps.seqsee.sobject import SAnchored, SElement, SGroup, SObject

class Workspace(object):
  def __init__(self):
    #: All elements. Each is a :class:`~apps.seqsee.sobject.SAnchored` object.
    self.elements = []
    #: Number of elements.
    self.num_elements = 0
    #: Groups (excluding single element groups).
    #: Each is a :class:`~apps.seqsee.sobject.SAnchored` object.
    self.groups = []

  def InsertElement(self, element):
    """Insert an element beyond the last element."""
    assert isinstance(element, SElement)
    anchored = SAnchored(element, self.num_elements, self.num_elements, is_sequence_element=True)
    self.num_elements += 1
    self.elements.append(anchored)
