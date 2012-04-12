# Utility functions for testing seqsee.
from apps.seqsee.anchored import SAnchored
from apps.seqsee.workspace import Workspace
from farg.ltm.graph import LTMGraph
from farg.controller import Controller
from farg.testing_utils import FringeAndCodeletsTest, CodeletPresenceSpec

class MockSeqseeController(Controller):
  def __init__(self, items):
    Controller.__init__(self, ui=None)
    workspace = self.workspace = Workspace()
    self.ltm = LTMGraph()
    workspace.InsertElements(*items)

# Too many public methods because of unittest. pylint: disable=R0904
class FringeOverlapTest(FringeAndCodeletsTest):

  @staticmethod
  def HelperCreateAndInsertGroup(workspace, specification, underlying_mapping=None):
    """Utility for quickly creating groups.

       Each element in the specification is a tuple consisting of integers or of other
       similarly structured tuples. Each generates a group, where the integers correspond to
       position in the workspace.

       A degenerate case is when the specification is an integer, in which case the WS
       element is returned.
    """
    if isinstance(specification, int):
      return workspace.elements[specification]
    else:
      anchored_items = list(FringeOverlapTest.HelperCreateAndInsertGroup(workspace, x)
                            for x in specification)
      new_group = SAnchored.Create(*anchored_items, underlying_mapping=underlying_mapping)
      return workspace.InsertGroup(new_group)

  @staticmethod
  def SetupTestingWS(items):
    workspace = Workspace()
    workspace.InsertElements(*items)
    return workspace
