from farg.apps.pyseqsee.arena import PSArena


class PSWorkspace(object):

  def __init__(self):
    self.arena = PSArena(magnitudes=())

  def InsertElements(self, magnitudes, log_msg=""):
    self.arena.Append(magnitudes=magnitudes, log_msg=log_msg)

  def KnownElementCount(self):
    return self.arena.KnownElementCount()

  def GetFirstElement(self):
    return self.arena.GetFirstElement()

  def SelectRandomElement(self):
    return self.arena.SelectRandomElement()

  def GetObjectToRight(self, item):
    return self.arena.GetObjectToRight(item)
