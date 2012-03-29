class RunMode:
  pass

class RunModeGUI(RunMode):
  def __init__(self):
    print("Initialized a GUI run mode")

class RunModeBatch(RunMode):
  def __init__(self):
    print("Initialized a Batch run mode")

class RunModeSxS(RunMode):
  def __init__(self):
    print("Initialized a SxS run mode")

