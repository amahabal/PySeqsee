import os.path
from farg.ltm.graph import LTMGraph

"""Manages the set of LTMs."""

class LTMManager(object):
  loaded_ltms = {}

  @classmethod
  def GetLTM(self, ltm_name):
    if ltm_name in LTMManager.loaded_ltms:
      return LTMManager.loaded_ltms[ltm_name]
    filename = '/home/amahabal/pyseqsee/ltms/%s' % ltm_name
    if not os.path.isfile(filename):
      # We need to create the LTM. I'd need to figure out how and where it should get
      # populated. For now, I will create an empty LTM.
      open(filename, 'w').close()
    ltm = LTMGraph(filename)
    LTMManager.loaded_ltms[ltm_name] = ltm
    return ltm

  @classmethod
  def SaveAllOpenLTMS(self):
    for k, v in LTMManager.loaded_ltms.iteritems():
      v.Dump()
