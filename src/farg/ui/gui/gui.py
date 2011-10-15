from Tkinter import Tk, Frame
class GUI(object):
  """A tkinter-based interfact for a FARG app.
  
  It sets up three frames: a buttons frame, a central pane, and an interaction
  widget. Subclasses can override specific bits of it as needed."""

  def __init__(self, controller, geometry='810x700+0+0'):
    self.mw = mw = Tk()
    self.controller = controller
    mw.geometry(geometry)
    self.SetupWindows()

  def Launch(self):
    """Starts the app by launching the UI."""
    self.mw.mainloop()

  def SetupWindows(self):
    """Sets up the three panes in the UI."""
    mw = self.mw

    self.buttons_pane = Frame(mw)
    self.PopulateButtonPane(self.buttons_pane)
    self.buttons_pane.grid()

    self.central_pane = Frame(mw)
    self.PopulateCentralPane(self.central_pane)
    self.central_pane.grid();

    self.interaction_pane = Frame(mw)
    self.PopulateInteractionPane(self.interaction_pane)
    self.interaction_pane.grid();

  def PopulateButtonPane(self, frame):
    """Adds buttons to the top row."""
    pass

  def PopulateCentralPane(self, frame):
    """Sets up the display in the central part."""
    pass

  def PopulateInteractionPane(self, frame):
    """Sets up the interaction pane at the bottom."""
    pass
