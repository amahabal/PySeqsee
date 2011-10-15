"""A sample app meant to test the framework as it is built.

I expect to replace this with something fuller as development progresses.
"""

from farg.controller import Controller
from farg.run_state import RunState
from farg.ui.gui.gui import GUI

def main():
  run_state = RunState()
  controller = Controller(run_state)
  gui = GUI(controller)
  gui.Launch()


if __name__ == "__main__":
  main()
