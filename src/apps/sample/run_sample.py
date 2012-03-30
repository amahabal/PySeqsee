from tide.main import Main
from third_party import gflags
import sys

FLAGS = gflags.FLAGS

class SampleMain(Main):
  def ProcessCustomFlags(self):
    pass

if __name__ == '__main__':
  SampleMain().main(sys.argv)
