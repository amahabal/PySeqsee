#!/usr/bin/env python

import gtk
import gtk.gdk

from third_party import xdot

graph = { 'a': ('b', 'c', 'd'),
          'b': ('a', 'd'),
          'c': (),
          'd': ('b', 'a') }

def GetGraph(startnode=None):
  if not startnode or startnode == '---':
    lines = []
    for k, v in graph.iteritems():
      lines.append('%s [URL="%s" color="#00ff00" style="filled"];' % (k, k))
      for other_node in v:
        lines.append('%s -> %s;' % (k, other_node))
    return """
    digraph G {
    %s
    }
    """ % ('\n'.join(lines))
  else:
    lines = ['%s [URL="%s" color="#ff0000" style="filled"];' % (startnode, startnode)]
    nodes_added = set(startnode)
    for other_node in graph[startnode]:
      if other_node not in nodes_added:
        nodes_added.add(other_node)
        lines.append('%s [URL="%s"];' % (other_node, other_node))
      lines.append('%s -> %s;' % (startnode, other_node))
    return """
    digraph G {
    %s
    }
    """ % ('\n'.join(lines))



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


dotcode = """
digraph G {
  A [URL="http://x.com"]
  B [URL="http://y.com"]
  A -> B
}
"""

def main():
    window = MyDotWindow()
    window.set_dotcode(GetGraph())
    window.connect('destroy', gtk.main_quit)
    gtk.main()

if __name__ == '__main__':
    main()
