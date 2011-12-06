#!/usr/bin/env python

from farg.ltm.graph import LTMGraph
from farg.ltm.storable import LTMStorableMixin
from third_party import xdot
import gtk
import gtk.gdk
import os
import tempfile

filehandle, filename = tempfile.mkstemp()
myltm = LTMGraph(filename)

class MockCategory(LTMStorableMixin):
  def __init__(self, foo):
    print "Initializing MockCategory instance ", self
    self.foo = foo

class MockCategory2(LTMStorableMixin):
  def __init__(self, foo):
    print "Initializing MockCategory2 instance ", self
    self.foo = foo

class MockMapping(LTMStorableMixin):
  def __init__(self, category):
    self.category = category

c1 = MockCategory.Create(foo=7)
m1 = MockMapping.Create(category=c1)
c2 = MockCategory.Create(foo=9)
m2 = MockMapping.Create(category=c2)

for content in (c1, m1, c2, m2):
  myltm.GetNodeForContent(content)

myltm.AddEdgeBetweenContent(m1, c1)
myltm.AddEdgeBetweenContent(m2, c2)
myltm.AddEdgeBetweenContent(c1, m2)
myltm.AddEdgeBetweenContent(c1, c2)
myltm.AddEdgeBetweenContent(c2, m1)

for content in (c1, m1, c2, m2):
  myltm.SpikeForContent(content, 50)
for content in (c1, m1):
  myltm.SpikeForContent(content, 100)


def GetGraph(startnode=None):
  if not startnode:
    xdot = myltm.GetGraphXDOT()
  else:
    xdot = myltm.GetGraphAroundNodeXDot(int(startnode))
  # print xdot
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

    def __init__(self):
        xdot.DotWindow.__init__(self)
        self.history_stack = []
        self.widget.connect('clicked', self.on_url_clicked)
        self.uimanager.remove_action_group(self.actiongroup)

        self.actiongroup = gtk.ActionGroup('Actions')
        self.actiongroup.add_actions((
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
        # print GetGraph(url)
        self.set_dotcode(GetGraph(url))
        self.history_stack.append(url)
        return True

    def display_full_graph(self, ignored_action):
      self.set_dotcode(GetGraph(None))
      self.history_stack = []

    def go_back(self, ignored_action):
      len_history = len(self.history_stack)
      if len_history == 0:
        return
      if len_history == 1:
        return self.display_full_graph(ignored_action)
      prior_url = self.history_stack[-2]
      self.history_stack = self.history_stack[:-1]
      self.set_dotcode(GetGraph(prior_url))

def main():
    window = MyDotWindow()
    window.set_dotcode(GetGraph())
    window.connect('destroy', gtk.main_quit)
    gtk.main()
    os.remove(filename)

if __name__ == '__main__':
    main()
