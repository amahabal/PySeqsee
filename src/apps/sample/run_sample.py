from tide.main import Main
from third_party import gflags
import sys

FLAGS = gflags.FLAGS

gflags.DEFINE_integer('random_seed', 10, "Random seed")

class SampleMain(Main):
  def ProcessCustomFlags(self):
    self.random_seed = FLAGS.random_seed
    print("Random seed=", self.random_seed)

if __name__ == '__main__':
  SampleMain().main(sys.argv)
