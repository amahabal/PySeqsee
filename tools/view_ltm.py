#!/usr/bin/python
import argparse
import gtk

from farg.ltm.graph import LTMGraph
from farg.ltm.view_ltm import GetGraph, MyDotWindow

def main():
  parser = argparse.ArgumentParser(description="An LTM viewer")
  parser.add_argument('filename', metavar='N', type=str,
                      help='Filename of ltm to view')
  args = parser.parse_args()

  # TODO(# --- Dec 30, 2011): Make sure file exists and so forth.
  ltm = LTMGraph(args.filename)
  print "LTM has %d nodes" % len(ltm._nodes)
  window = MyDotWindow(ltm)
  window.set_dotcode(GetGraph(ltm))
  window.connect('destroy', gtk.main_quit)
  gtk.main()

if __name__ == '__main__':
  main()

