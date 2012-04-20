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

"""Manages the set of LTMs."""

from farg.core.ltm.graph import LTMGraph
from farg.third_party import gflags
import logging
import os.path
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
