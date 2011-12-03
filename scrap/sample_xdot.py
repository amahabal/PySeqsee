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
    lines.append('GoBack [URL="---"];')
    return """
    digraph G {
    %s
    }
    """ % ('\n'.join(lines))



class MyDotWindow(xdot.DotWindow):

    def __init__(self):
        xdot.DotWindow.__init__(self)
        self.widget.connect('clicked', self.on_url_clicked)

    def on_url_clicked(self, widget, url, event):
#        dialog = gtk.MessageDialog(
#                parent=self,
#                buttons=gtk.BUTTONS_OK,
#                message_format="%s clicked" % url)
#        dialog.connect('response', lambda dialog, response: dialog.destroy())
#        dialog.run()
        print GetGraph(url)
        self.set_dotcode(GetGraph(url))
        return True

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
