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

import logging

from farg.core.ltm.graph import LTMGraph
import os.path
import sys

import farg_flags

kLogger = logging.getLogger("LTM")

class LTMManager(object):
  #: What LTMs have been loaded.
  loaded_ltms = {}
  loaded_ltms_copy = {}
  #: Registered LTM initalizers (registered via RegisterInitializer).
  _registered_initializers = {}

  @classmethod
  def GetLTM(cls, ltm_name):
    kLogger.info("GetLTM called with %s", ltm_name)
    if ltm_name in LTMManager.loaded_ltms_copy:
      return LTMManager.loaded_ltms_copy[ltm_name]
    if farg_flags.FargFlags.use_stored_ltm:
      filename = os.path.join(farg_flags.FargFlags.ltm_directory, ltm_name)
      if not os.path.isfile(filename):
        # We need to create the LTM. I'd need to figure out how and where it should get
        # populated. For now, I will create an empty LTM.
        open(filename, 'w').close()
      ltm = LTMGraph(filename=filename)
    else:
      ltm = LTMGraph(empty_ok_for_test=True)
    if ltm.IsEmpty():
      if ltm_name in cls._registered_initializers:
        cls._registered_initializers[ltm_name](ltm)
        # Also save the LTM immediately.
        ltm.DumpToFile()
        kLogger.info("LTM %s was empty, initialized.", ltm_name)
      else:
        kLogger.warn("LTM %s was empty, and no initalizer registered.", ltm_name)
    ltm_copy = LTMGraph(master_graph=ltm)
    LTMManager.loaded_ltms[ltm_name] = ltm
    LTMManager.loaded_ltms_copy[ltm_name] = ltm_copy
    return ltm_copy

  @classmethod
  def RegisterInitializer(cls, ltm_name, initializer_function):
    """Registers an initializer to call if a loaded LTM is empty. The function takes a
       single argument, the LTM.
    """
    LTMManager._registered_initializers[ltm_name] = initializer_function

  @classmethod
  def SaveAllOpenLTMS(cls):
    for _ltm_name, ltm_copy in LTMManager.loaded_ltms_copy.items():
      orig_ltm = ltm_copy.master_graph
      if not hasattr(orig_ltm, 'filename') or not orig_ltm.filename:
        continue
      ltm_copy.UploadToMaster()
      orig_ltm.DumpToFile()
