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

from farg.core.run_mode.run_mode import RunMode

class RunModeGUI(RunMode):
  def __init__(self, *, controller_class, ui_class, stopping_condition_fn=None):
    print("Initialized a GUI run mode")
    self.ui = ui_class(controller_class=controller_class,
                       stopping_condition_fn=stopping_condition_fn)

  def Run(self):
    self.Refresher()
    self.ui.mw.mainloop()

  def Refresher(self):
    self.ui.UpdateDisplay()
    self.ui.mw.after(100, self.Refresher)
