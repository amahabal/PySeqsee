"""Manages the set of LTMs."""

import os.path
from farg.ltm.graph import LTMGraph

import logging
from third_party import gflags
import sys
logger = logging.getLogger(__name__)

FLAGS = gflags.FLAGS

class LTMManager(object):
  #: What LTMs have been loaded.
  loaded_ltms = {}
  #: Registered LTM initalizers (registered via RegisterInitializer).
  _registered_initializers = {}

  @classmethod
  def GetLTM(cls, ltm_name):
    if ltm_name in LTMManager.loaded_ltms:
      return LTMManager.loaded_ltms[ltm_name]
    # TODO(# --- Feb 9, 2012): Should not be hardcoded.
    filename = os.path.join(FLAGS.ltm_directory, ltm_name)
    if not os.path.isfile(filename):
      # We need to create the LTM. I'd need to figure out how and where it should get
      # populated. For now, I will create an empty LTM.
      open(filename, 'w').close()
    ltm = LTMGraph(filename)
    if ltm.IsEmpty():
      if ltm_name in cls._registered_initializers:
        cls._registered_initializers[ltm_name](ltm)
        # Also save the LTM immediately.
        ltm.Dump()
        logging.warning("LTM %s was empty, initialized.", ltm_name)
      else:
        logging.warning("LTM %s was empty, and no initalizer registered.", ltm_name)
    LTMManager.loaded_ltms[ltm_name] = ltm
    return ltm

  @classmethod
  def RegisterInitializer(cls, ltm_name, initializer_function):
    """Registers an initializer to call if a loaded LTM is empty. The function takes a
       single argument, the LTM.
    """
    LTMManager._registered_initializers[ltm_name] = initializer_function

  @classmethod
  def SaveAllOpenLTMS(cls):
    for _ltm_name, ltm in LTMManager.loaded_ltms.items():
      ltm.Dump()
