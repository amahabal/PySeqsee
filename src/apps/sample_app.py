"""A sample app meant to test the framework as it is built.

I expect to replace this with something fuller as development progresses.
"""
import time

from farg.controller import Controller
from farg.run_state import RunState
from farg.ui.gui.gui import GUI
from farg.exceptions import FargException

class MyController(Controller):
  def Step(self):
    print "Taking a step."
    time.sleep(5)
    raise FargException()

def main():
  run_state = RunState()
  controller = MyController(run_state)
  gui = GUI(controller)
  gui.Launch()


if __name__ == "__main__":
  main()
