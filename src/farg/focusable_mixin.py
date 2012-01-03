from farg.exceptions import FargError
class FocusableMixin(object):
  """A mixin for things that want to be part of the stream. It is a pure interface --- all
     methods die horribly when called since they expect to have been over-ridden.
  """


  def GetFringe(self, controller):
    """Returns the fringe of the item, which should be a dictionary keyed by fringe elements
       and with floats as values (indicating intensity of the element within the fringe).
    """
    raise FargError("Focusable mixin's GetFringe() was not over-ridden.")


  def GetAffordances(self, controller):
    """Returns a list of codelets that make sense for this type of object."""
    raise FargError("Focusable mixin's GetAffordances() was not over-ridden.")


  def GetSimilarityAffordances(self, focusable, other_fringe, my_fringe, controller):
    """When the fringe of a stored focus overlaps the fringe of a newly focused entity,
       this function is called. Here, self is the older focus, and my_fringe is its fringe.
       focusable is the new focusable, and other_fringe is its fringe.
       
       This should return a list of codelets that follow-up on this potential similarity.
    """
    raise FargError("Focusable mixin's GetSimilarityAffordances() was not over-ridden.")
