from Tkinter import Tk, Button, Frame, Label, LEFT, TOP, StringVar, Toplevel, BOTTOM
from farg.exceptions import YesNoException
from farg.ui.gui.dot_to_graph import GraphViewer
from farg.ui.ui import UI
import tkMessageBox


class GUI(UI):
  """A tkinter-based interface for FARG applications.

     It sets up three frames: a buttons frame, a central pane, and an interaction
     widget. Subclasses can override specific bits of it as needed.
  """

  def __init__(self, controller, flags, geometry='810x700+0+0'):
    UI.__init__(self, controller, flags)
    #: The main-window of the UI.
    self.mw = mw = Tk()
    mw.geometry(geometry)
    self.SetupWindows(flags)
    if flags.gui_show_ltm:
      self.SetupLTMWindow(flags)

  def Launch(self):
    """Starts the app by launching the UI."""
    self.mw.mainloop()

  def ReDraw(self):
    """Redraws the UI, flushing any changes that need to be."""
    for item in self.items_to_refresh:
      item.ReDraw()
    self.codelet_count_var.set('%d' % self.controller.steps_taken)

  def CleanupAfterQuit(self):
    """Called after Quit (by Quit) for any cleanup."""
    self.mw.quit()


  def HandleAppSpecificFargException(self, exception):
    """A hook to allow derivative classes a way to handle specific types of exceptions.

       If unhandled, the exception should be rethrown.

       By default, this does nothing and rethrows the exception.
    """
    raise exception

  def HandleFargException(self, exception):
    """Takes care of the exception thrown by the controller, provided it is the right type."""
    try:
      raise exception
    except YesNoException:
      answer = tkMessageBox.askyesno("Question", exception.question_string)
      exception.callback(answer)
    except:
      print '----------'
      for line in exception.stack_trace:
        print line
      print '----------'
      raise exception

  def SetupWindows(self, args):
    """Sets up the three panes in the UI."""
    mw = self.mw
    self.items_to_refresh = []

    self.buttons_pane = Frame(mw)
    self.PopulateButtonPane(self.buttons_pane)
    self.buttons_pane.grid()

    self.PopulateCentralPane(args)
    self.PopulateInteractionPane(args)

  def SetupLTMWindow(self, args):
    """Creates a LTM-viewer window."""
    ltm_top = Toplevel()
    button_frame = Frame(ltm_top)
    button_frame.pack(side=TOP)
    Button(button_frame, text='Full Graph',
           command=lambda: self.graph_viewer.DrawGraph()).pack(side=LEFT)

    self.graph_viewer_message = StringVar()
    Label(ltm_top, textvariable=self.graph_viewer_message).pack(side=BOTTOM)
    self.graph_viewer_message.set("")

    graph_viewer = self.graph_viewer = GraphViewer(ltm_top, 400, 400, self.controller.ltm,
                                                   self.graph_viewer_message)
    graph_viewer.pack(side=TOP)
    graph_viewer.DrawGraph()
    self.items_to_refresh.append(graph_viewer)


  def PopulateButtonPane(self, frame):
    """Adds buttons to the top row."""
    Button(frame, text="Start", command=self.Start).pack(side=LEFT)
    Button(frame, text="Pause", command=self.Pause).pack(side=LEFT)
    Button(frame, text="Quit", command=self.Quit).pack(side=LEFT)
    self.codelet_count_var = StringVar()
    self.codelet_count_var.set("0")
    Label(frame, textvariable=self.codelet_count_var,
          font='-adobe-helvetica-bold-r-normal--28-140-100-100-p-105-iso8859-4',
          fg='#FF0000').pack(side=LEFT)

  def PopulateCentralPane(self):
    """Sets up the display in the central part.
    
    If an item must be refreshed, add it to items_to_refresh."""
    pass

  def PopulateInteractionPane(self):
    """Sets up the interaction pane at the bottom."""
    pass

  def DisplayMessage(self, message):
    tkMessageBox.showinfo('', message)

  def AskYesNoQuestion(self, question):
    return tkMessageBox.askyesno("Question", question)
