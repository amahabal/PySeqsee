#!/usr/bin/python
from apps.seqsee.controller import SeqseeController
from apps.seqsee.gui.gui import SeqseeGUI
from apps.seqsee.read_input_spec import ReadInputSpec
from apps.seqsee.stopping_conditions import stopping_conditions_dict
from third_party import gflags
from tide.main import Main
import sys

FLAGS = gflags.FLAGS

gflags.DEFINE_spaceseplist('sequence', '',
                           'A space separated list of integers')

gflags.DEFINE_spaceseplist('unrevealed_terms', '',
                           'A space separated list of integers')

class SeqseeMain(Main):
  gui_class = SeqseeGUI
  controller_class = SeqseeController
  stopping_conditions = stopping_conditions_dict
  input_spec_reader_class = ReadInputSpec

  def ProcessCustomFlags(self):
    FLAGS.sequence = [int(x) for x in FLAGS.sequence]
    FLAGS.unrevealed_terms = [int(x) for x in FLAGS.unrevealed_terms]

if __name__ == '__main__':
  SeqseeMain().main(sys.argv)
