# First cut of a Tk based viewer. Draws nodes and edges, but little else.

import colorsys
import math
import sys
import subprocess
from Tkinter import Tk, Canvas, ALL

from third_party.xdot import XDotParser
from farg.ltm.graph import LTMGraph
from farg.ui.gui.util import HSVToColorString

class GraphViewer(Canvas):

  def __init__(self, master, width, height, ltm, message_label):
    Canvas.__init__(self, master, width=width, height=height)
    self.width = width - 10
    self.height = height - 10
    self.ltm = ltm
    self.message_label = message_label
    self.startnode = None

  def DrawGraph(self, startnode=None):
    self.startnode = startnode
    self.delete(ALL)
    if startnode is not None:
      dotcode = self.ltm.GetGraphAroundNodeXDot(int(startnode))
    else:
      dotcode = self.ltm.GetGraphXDOT()
    graph = self._ConvertToGraph(dotcode)
    self._CalculateTransformParameters(graph)
    for node in graph.nodes:
      self._DrawNode(node)
    for edge in graph.edges:
      self._DrawEdge(edge)

  def ReDraw(self):
    self.DrawGraph(self.startnode)

  def _CalculateTransformParameters(self, graph):
    width, height = graph.get_size()
    self.graph_width = width
    self.graph_height = height
    x_multiplier = self.width / width
    y_multiplier = self.height / height
    multiplier = min(x_multiplier, y_multiplier)
    if x_multiplier == multiplier:
      self.x_multiplier = multiplier
      self.y_multiplier = multiplier
      self.x_offset = 5
      self.y_offset = 5 + 0.5 * (self.height - (height * multiplier))
    else:
      self.x_multiplier = multiplier
      self.y_multiplier = multiplier
      self.x_offset = 5 + 0.5 * (self.width - (width * multiplier))
      self.y_offset = 5



  def _Transform(self, x, y):
    return (self.x_offset + x * self.x_multiplier,
            self.y_offset + y * self.y_multiplier)

  def _DisplayNodeDetails(self, ltm_node):
    label = ltm_node.content.BriefLabel()
    raw_activation = ltm_node.GetRawActivation(0)
    activation = ltm_node.GetActivation(0)
    depth = math.trunc(0.5 + 1.0 / ltm_node.depth_reciprocal)
    description = 'Node=%s raw=%.2f act=%.2f depth=%d' % (label, raw_activation,
                                                          activation, depth)
    self.message_label.set(description)

  def _DrawNode(self, node):
    x, y = self._Transform(node.x, node.y)
    x1, y1 = self._Transform(node.x1, node.y1)
    x2, y2 = self._Transform(node.x2, node.y2)
    ltm_node = self.ltm._nodes[int(node.url)]
    label = ltm_node.content.BriefLabel()
    color = HSVToColorString(0.2, ltm_node.GetActivation(0), 1.0)
    oval = self.create_oval(x1, y1, x2, y2, fill=color)
    self.tag_bind(oval, '<1>', lambda e: self.DrawGraph(int(node.url)))
    self.tag_bind(oval, '<Enter>', lambda e: self._DisplayNodeDetails(ltm_node))
    drawn_text = self.create_text(x, y, text=label)
    self.tag_bind(drawn_text, '<1>', lambda e: self.DrawGraph(int(node.url)))

  def _DrawEdge(self, edge):
    #print 'src=', edge.src
    #print 'dst=', edge.dst
    #print 'points=', edge.points
    point_coordinates = []
    for x, y in edge.points:
      tx, ty = self._Transform(x, y)
      point_coordinates.extend((tx, ty))
    self.create_line(point_coordinates, smooth=1, width=max(2, 2.0 * self.x_multiplier),
                     arrow="last")

  def _ConvertToXDot(self, dotcode):
    p = subprocess.Popen(['dot', '-Txdot'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         shell=False,
                         universal_newlines=True)
    xdotcode, error = p.communicate(dotcode)
    sys.stderr.write(error)
    if p.returncode != 0:
      return None
    return xdotcode

  def _ConvertToGraph(self, dotcode):
    xdotcode = self._ConvertToXDot(dotcode)
    parser = XDotParser(xdotcode)
    graph = parser.parse()
    return graph


def main():
  import argparse
  parser = argparse.ArgumentParser(description="An LTM viewer")
  parser.add_argument('filename', metavar='N', type=str,
                      help='Filename of ltm to view')
  args = parser.parse_args()

  # TODO(# --- Dec 30, 2011): Make sure file exists and so forth.
  ltm = LTMGraph(args.filename)
  print "LTM has %d nodes" % len(ltm._nodes)

  mw = Tk()
  viewer = GraphViewer(mw, 700, 500, ltm)
  viewer.pack()
  viewer.DrawGraph(7)
  mw.mainloop()


if __name__ == '__main__':
    main()
