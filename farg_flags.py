"""Defines the flags shared by all apps."""

import argparse

core_parser = argparse.ArgumentParser(add_help=False)
core_parser.add_argument('--run_mode',
                         choices=('gui', 'batch', 'sxs', 'single'),
                         default='gui',
                         help='Mode to run in. GUI creates a tkinter display, whereas batch and '
                              'sxs run the program multiple times non-interactively. Each such run'
                              ' uses the "single" run mode.')
core_parser.add_argument('--debug',
                         choices=('', 'debug', 'info', 'warn', 'error', 'fatal'),
                         default='',
                         help='Show messages from this debug level and above')
core_parser.add_argument('--debug_config',
                         help='If defined, used to configure loggers')
core_parser.add_argument('--persistent_directory',
                         help='Directory in which to hold files that persist between runs, such as '
                              'ltm files or statistics about performance on batch runs. '
                              'If not passed, ~/.pyseqsee/{application_name} is used.')
core_parser.add_argument('--ltm_directory',
                         help='Directory to hold LTM files. '
                              'If not passed, FLAGS.persistent_directory/ltm is used')
core_parser.add_argument('--stats_directory',
                         help='Directory to hold statistics from prior batch runs. '
                              'If not passed, FLAGS.persistent_directory/stats is used')
core_parser.add_argument('--input_spec_file',
                         help='Path specifying inputs over which to run batch processes.'
                              'This will be read by an instance of input_spec_reader_class.')
core_parser.add_argument('--num_iterations', default=10, type=int,
                         help='In batch and SxS mode, number of iterations to run')
core_parser.add_argument('--max_steps', default=20000, type=int,
                         help='In batch and SxS mode, number of steps per run')

core_parser.add_argument('--stopping_condition',
                         help='Stopping condition, if any. Only allowed in non-gui modes. If the '
                              'condition is met, the program returns with a StoppingConditionMet '
                              'exception')
core_parser.add_argument('--use_stored_ltm', default=True, type=bool,
                         help="If true, load LTMs from disk. If not, a brand new one is created.")

core_parser.add_argument('--base_flags', help='Extra flags for base')
core_parser.add_argument('--exp_flags', help='Extra flags for exp')
core_parser.add_argument('--eat_output', default=True, type=bool,
                         help='If true, eat up most output.')

core_parser.add_argument('--gui_canvas_height', default=850, type=int,
                         help='Height of the central canvas')
core_parser.add_argument('--gui_canvas_width', default=1270, type=int,
                         help='Width of the central canvas')

core_parser.add_argument('--gui_initial_view', help="Initial view in GUI mode")
core_parser.add_argument('--stopping_condition_granularity', default=5, type=int,
                         help='How frequently the stopping condition is evaluated, as measured in'
                              ' number of codelets.')
