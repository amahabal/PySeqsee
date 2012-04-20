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

from farg.third_party import gflags
FLAGS = gflags.FLAGS

class BatchUI:
  def __init__(self, *, controller_class, stopping_condition_fn=None):
    self.pause_stepping = False
    self.quitting = False
    self.stepping_thread = None

    self.controller = controller_class(ui=self, controller_depth=0,
                                       stopping_condition=stopping_condition_fn)
    self.RegisterQuestionHandlers()

  def AskQuestion(self, question):
    return question.Ask(self)

  def RegisterQuestionHandlers(self):
    pass

  def Run(self):
    self.controller.RunUptoNSteps(FLAGS.max_steps)
