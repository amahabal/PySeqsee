from farg.apps.pyseqsee.categorization.categorizable import Categorizable

class PSRelation(Categorizable):
  def __init__(self, *, first, second):
    self.first = first
    self.second = second
    Categorizable.__init__(self)
