import os.path
import sys
from farg.core.ltm.graph import LTMGraph

def GetLTMPath(app_name, ltm_name):
  homedir = os.path.expanduser('~')
  if not os.path.exists(homedir):
    print ('Could not locate home directory for storing LTM files.'
           'You could explicitly specify an existing directory to use by using'
           'the flag --ltm_directory. Quitting.')
    sys.exit(1)
  pyseqsee_home = os.path.join(homedir, '.pyseqsee')
  if not os.path.exists(pyseqsee_home):
    print ('Directory missing: %s, could not locate LTM file' % pyseqsee_home)
    sys.exit(1)
  directory = os.path.join(pyseqsee_home, app_name, 'ltm')
  if not os.path.exists(directory):
    print ('Directory missing: %s, could not locate LTM file' % directory)
    sys.exit(1)
  filename = os.path.join(directory, ltm_name)
  if not os.path.exists(filename):
    print ('LTM file %s missing' % filename)
    sys.exit(1)
  return filename

def PrintLTM(args):
  """Prints out LTM."""
  filename = GetLTMPath(args.app_name, args.ltm_name)
  ltm = LTMGraph(filename=filename)
  print("LTM contains %d nodes" % len(ltm.nodes))
  for idx, node in enumerate(ltm.nodes):
    print('-- %d [dep=%5.3f] --' % (idx, 1.0 / node.depth_reciprocal), node.content.BriefLabel())
    for edge in node.GetOutgoingEdges():
      other_node = edge.to_node
      print('\tEdge:%s to %s [Utility=%d]' % (edge.edge_type, other_node.content.BriefLabel(),
                                              edge.utility))