#!/usr/bin/python

from apps.seqsee.controller import SeqseeController
from apps.seqsee.gui.gui import SeqseeGUI
from third_party import gflags
import sys
from tide.main import Main

FLAGS = gflags.FLAGS

gflags.DEFINE_spaceseplist('sequence', '',
                           'A space separated list of integers')

gflags.DEFINE_spaceseplist('unrevealed_terms', '',
                           'A space separated list of integers')

class SeqseeMain(Main):
  gui_class = SeqseeGUI
  controller_class = SeqseeController

  def ProcessCustomFlags(self):
    FLAGS.sequence = [int(x) for x in FLAGS.sequence]
    FLAGS.unrevealed_terms = [int(x) for x in FLAGS.unrevealed_terms]

if __name__ == '__main__':
  SeqseeMain().main(sys.argv)
