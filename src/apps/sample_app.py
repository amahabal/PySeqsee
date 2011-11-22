"""A sample app meant to test the framework as it is built.

I expect to replace this with something fuller as development progresses.
"""
import time
import tkMessageBox

from farg.controller import Controller
from farg.runstate import RunState
from farg.ui.gui.gui import GUI
from farg.exceptions import *

class FooException(FargException):
  pass

class BarException(FargException):
  pass

class MyController(Controller):
  def BlueSkyCallback(self, answer):
    print "Blue sky callback. I am %s. Answer=%s" % (self, answer)

  def Step(self):
    print "Taking a step. I am %s" % self
    # raise YesNoException("Is the sky blue?", self.BlueSkyCallback)
    raise FooException()

class MyGUI(GUI):
  def HandleAppSpecificFargException(self, exception):
    try:
      raise exception
    except FooException:
      tkMessageBox.showinfo("Hi", "Reached a FooException")



def main():
  runstate = RunState()
  controller = MyController(runstate)
  gui = MyGUI(controller)
  gui.Launch()


if __name__ == "__main__":
  main()
