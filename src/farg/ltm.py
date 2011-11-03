"""Long term memory."""

import cPickle as pickle

class LTM(object):
  def __init__(self, filename):
    self.nodes = []
    self.filename = filename
    with open(filename) as f:
      up = pickle.Unpickler(f)
      self.Load(up)

  def Load(self, unpickler):
    while True:
      try:
        node = unpickler.load()
        self.AddNode(node)
      except EOFError:
        print "Done reading"
        break

  def Dump(self):
    with open(self.filename, "w") as f:
      pickler = pickle.Pickler(f, 2)
      for node in self.nodes:
        pickler.dump(node)

  def AddNode(self, node):
    self.nodes.append(node)
