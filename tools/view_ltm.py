#!/usr/bin/python
import argparse
from third_party import xdot
import gtk
import gtk.gdk

from farg.ltm.graph import LTMGraph

def GetGraph(ltm, startnode=None):
  if not startnode:
    xdot = ltm.GetGraphXDOT()
  else:
    xdot = ltm.GetGraphAroundNodeXDot(int(startnode))
  return xdot

class MyDotWindow(xdot.DotWindow):
  ui = '''
    <ui>
        <toolbar name="ToolBar">
            <toolitem action="Reload"/>
            <toolitem action="FullGraph"/>
            <toolitem action="GoBack"/>
            <separator/>
            <toolitem action="ZoomIn"/>
            <toolitem action="ZoomOut"/>
            <toolitem action="ZoomFit"/>
            <toolitem action="Zoom100"/>
        </toolbar>
    </ui>
    '''

  def __init__(self, ltm):
    xdot.DotWindow.__init__(self)
    self.history_stack = []
    self.widget.connect('clicked', self.on_url_clicked)
    self.uimanager.remove_action_group(self.actiongroup)
    self.ltm = ltm

    self.actiongroup = gtk.ActionGroup('Actions')
    self.actiongroup.add_actions(
        (
         ('FullGraph', gtk.STOCK_HOME, None, None, None, self.display_full_graph),
         ('GoBack', gtk.STOCK_GO_BACK, None, None, None, self.go_back),
         ('Reload', gtk.STOCK_REFRESH, None, None, None, self.on_reload),
         ('ZoomIn', gtk.STOCK_ZOOM_IN, None, None, None, self.widget.on_zoom_in),
         ('ZoomOut', gtk.STOCK_ZOOM_OUT, None, None, None, self.widget.on_zoom_out),
         ('ZoomFit', gtk.STOCK_ZOOM_FIT, None, None, None, self.widget.on_zoom_fit),
         ('Zoom100', gtk.STOCK_ZOOM_100, None, None, None, self.widget.on_zoom_100),
        ))
    self.uimanager.insert_action_group(self.actiongroup, 0)
    self.uimanager.add_ui_from_string(self.ui)


  def on_url_clicked(self, widget, url, event):
    self.set_dotcode(GetGraph(self.ltm, url))
    self.history_stack.append(url)
    return True

  def display_full_graph(self, ignored_action):
    self.set_dotcode(GetGraph(self.ltm, None))
    self.history_stack = []

  def go_back(self, ignored_action):
    len_history = len(self.history_stack)
    if len_history == 0:
      return
    if len_history == 1:
      return self.display_full_graph(ignored_action)
    prior_url = self.history_stack[-2]
    self.history_stack = self.history_stack[:-1]
    self.set_dotcode(GetGraph(self.ltm, prior_url))

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

