from farg.apps.pyseqsee.arena import PSArena
from farg.core.util import UnweightedChoice


class PSWorkspace(object):

  def __init__(self):
    self.arena = PSArena(magnitudes=())

  def KnownElementCount(self):
    return len(self.arena.element)

  def InsertElements(self, magnitudes):
    self.arena.Append(magnitudes=magnitudes)

  def GetFirstElement(self):
    return self.arena.element[0]

  def SelectRandomElement(self):
    return UnweightedChoice(self.arena.element)
