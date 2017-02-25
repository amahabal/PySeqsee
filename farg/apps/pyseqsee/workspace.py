from farg.apps.pyseqsee.arena import PSArena

class PSWorkspace(object):
  def __init__(self):
    self.arena = PSArena(magnitudes=())

  def InsertElements(self, magnitudes):
    self.arena.Append(magnitudes=magnitudes)
