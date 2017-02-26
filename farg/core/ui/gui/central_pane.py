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

"""Central pane of the UI display.

This is a canvas that can hold multiple views (such as Coderack view, Workspace view, and so forth).

Each view is an instance of a subclass of :py:class:`~farg.core.ui.gui.views.viewport.ViewPort`.
"""
import farg.flags as farg_flags
from farg.core.history import HistoryGUI
import sys
from tkinter import ALL, Canvas, Menu

class CentralPane(Canvas):  # Pylint thinks this has 9 ancestrors. pylint:disable=R0901,R0904
  """The central area of the UI based display.

  **ViewPorts** and **Views**

  A Viewport is a small window through which to look at some aspects the activity of the app.
  Examples of viewports that come packaged with PySeqsee include :py:class:`~farg.core.ui.gui.views.coderack_view.CoderackView`,
  which displays the current codelets waiting to run. Other already supplied views can be found in
  the :py:mod:`~farg.core.ui.gui.views` module.

  A View, on the other hand, is a tiling of a few such views into a display. A View may consist of
  just a single viewport, or two or more viewports. This class provides methods to create views and
  to maintain a set of named views.

  **Setting up views**

  A view may be set up by calling one of the following methods of this class. SetFullView, which
  takes a viewport class as argument, creates a view with that single, full-sized viewport. The
  names SetVerticallySplitView and SetThreeWaySplit should be self-explanatory.

  **Example Usage**

  For an example of how a subclass may set up the views, take a look at the code for
  :py:class:`farg.apps.seqsee.gui.gui.SeqseeCentralPane`.
  """

  #: A dictionary from names to functions that sets views. A view is made up of a set of
  #: viewports, each an instance of :py:class:`~farg.core.ui.gui.views.viewport.ViewPort`.
  #: Methods are available in this class to create views (e.g., SetFullView and
  #: SetVerticallySplitView). See farg.apps.seqsee.gui.gui.py for an example.
  named_views = {}  # Not a constant. pylint: disable=C6409

  #: Name of initial view.
  default_initial_view = ''  # Not a constant. pylint: disable=C6409
  def __init__(self, master, controller, *, height, width, background):
    self.is_history_displayed = False
    self.height = height
    self.width = width
    self.controller = controller
    self.viewports = []
    Canvas.__init__(self, master, height=height, width=width, background=background)
    self.SetupMenu(master)
    self.SetNamedView(farg_flags.FargFlags.gui_initial_view or self.default_initial_view)
    if farg_flags.FargFlags.history:
      self.TurnOnHistoryGUI()

  def ReDraw(self):
    """Redraw all active views on pane."""
    self.delete(ALL)
    for viewport in self.viewports:
      viewport.ReDraw(self.controller)
    if self.is_history_displayed:
      self.history_gui.Refresh()

  def SetFullView(self, view_class):
    """Set central pane to contain a single view.

    Args:
      view_class: A subclass of :py:class:`~farg.core.ui.gui.views.viewport.ViewPort`.
    """
    self.viewports = [view_class(self, 0, 0, self.width, self.height)]
    self.ReDraw()

  def SetVerticallySplitView(self, view_class1, view_class2):
    """Set central pane to contain a two view, one on top the other on the bottom.

    Args:
      view_class1: A subclass of :py:class:`~farg.core.ui.gui.views.viewport.ViewPort`.
      view_class2: Another subclass of :py:class:`~farg.core.ui.gui.views.viewport.ViewPort`.
    """
    self.viewports = [view_class1(self, 0, 0, self.width, self.height / 2 - 2),
                      view_class2(self, 0, self.height / 2 + 2,
                                  self.width, self.height / 2 - 2)]
    self.ReDraw()

  def SetThreeWaySplit(self, view_class1, view_class2, view_class3):
    """Set central pane to contain a three view, one on top and two on the bottom.

    Args:
      view_class1: A subclass of :py:class:`~farg.core.ui.gui.views.viewport.ViewPort`.
      view_class2: Another subclass of :py:class:`~farg.core.ui.gui.views.viewport.ViewPort`.
      view_class3: Also a subclass of :py:class:`~farg.core.ui.gui.views.viewport.ViewPort`.
    """
    self.viewports = [view_class1(self, 0, 0, self.width, self.height / 2 - 2),
                      view_class2(self, 0, self.height / 2 + 2,
                                  self.width / 2 - 2, self.height / 2 - 2),
                      view_class3(self, self.width / 2 + 2, self.height / 2 + 2,
                                  self.width / 2 - 2, self.height / 2 - 2)]
    self.ReDraw()

  def SetNamedView(self, name):
    """Set the named view by calling the function shored in named_views."""
    if not name in self.named_views:
      print('Unrecognized view %s' % name)
      print('Available views: ', list(self.named_views.keys()))
      sys.exit(1)
    self.named_views[name](self)

  def NamedViewCmd(self, name):
    return (lambda: self.SetNamedView(name))

  def TurnOnHistoryGUI(self):
    self.is_history_displayed = True
    self.history_gui = HistoryGUI()

  def SetupMenu(self, parent):
    """Create menu for the central pane."""
    menubar = Menu(self)

    view_menu = Menu(menubar, tearoff=0)
    for name in self.named_views:
      view_menu.add_command(label=name,
                            command=self.NamedViewCmd(name))
    view_menu.add_command(label='History',
                          command=self.TurnOnHistoryGUI)
    menubar.add_cascade(label='View', menu=view_menu)

    try:
      debug_menu = Menu(menubar, tearoff=0)
      debug_menu.add_command(label='Debug Relations',
                             command=self.controller.workspace.DebugRelations)
      menubar.add_cascade(label='Debug', menu=debug_menu)
    except AttributeError:
      pass

    parent.config(menu=menubar)
