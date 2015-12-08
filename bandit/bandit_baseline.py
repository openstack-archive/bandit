# -*- coding:utf-8 -*-
#
# Copyright 2015 Hewlett-Packard Enterprise
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import argparse
import atexit
import logging
import os
import subprocess
import sys

bandit_args = sys.argv[1:]
baseline_tmp_file = '/tmp/_bandit_baseline_run.json_'
default_output_format = 'terminal'
logger = logging.getLogger(__name__)
original_branch = None
output_format = None
report_basename = 'bandit_baseline_result'
report_fname = ''
valid_baseline_formats = ['txt', 'html']


def main():
    global original_branch
    global output_format
    global report_fname

    init_logger()

    output_format = determine_output_format()
    if not output_format:
        # return same output code Bandit uses for running errors
        sys.exit(2)

    report_fname = "{}.{}".format(report_basename, output_format)

    if not valid_requirements():
        sys.exit(2)

    _, output, _ = call_command(['git', 'rev-parse', '--abbrev-ref',
                                 'HEAD'])
    original_branch = output.strip()

    parent_commit = get_parent_commit()

    statuses = ['', 'Running Bandit on parent commit', '',
                'Running Bandit on current commit']

    commands = [['git', 'checkout', parent_commit],

                ['bandit'] + bandit_args + ['-f', 'json', '-o',
                                            baseline_tmp_file],

                ['git', 'checkout', original_branch],

                ['bandit'] + bandit_args + ['-b', baseline_tmp_file]]

    # if user didn't specify an output format, we'll just display results on
    # the terminal, otherwise specify the output report file
    if output_format == 'terminal':
        commands[3] += ['-f', 'txt']
    else:
        commands[3] += ['-o', report_fname]

    for index, cmd in enumerate(commands):
        # display a status message if we're going into a potentially lengthy
        # operation
        if statuses[index]:
            logger.info(statuses[index])

        return_code, output, err = call_command(cmd)

        if return_code not in [0, 1]:
            logger.error("Error running command: %s\nOutput: %s\nError: %s",
                         cmd, output, err)
            sys.exit(return_code)

    if output_format == 'terminal':
        print(output)
    else:
        logger.info("Successfully wrote %s", report_fname)


def call_command(command_list):
    output = None
    err = None

    cmd = subprocess.Popen(command_list, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)

    output, err = cmd.communicate()

    return cmd.returncode, output, err


@atexit.register
def clean_up():
    global original_branch
    call_command(['rm', baseline_tmp_file])
    call_command(['git', 'checkout', str(original_branch)])


def get_parent_commit():
    # call the following command safely:
    # git log -2 --first-parent --pretty=oneline | cut -d " " -f1 | sed -n 2p

    return_code, cmd_output, err = call_command(['git', 'rev-parse', 'HEAD^'])

    # we want the first word of the second line
    parent_commit = cmd_output.strip('\n')
    logger.info('Using parent commit: %s as baseline', parent_commit)

    if return_code:
        logger.error('Unable to get parent commit ID')
        sys.exit(2)
    else:
        return parent_commit


def determine_output_format():
    # if no output format is given, use the default
    if '-f' not in sys.argv:
        logger.info("No output format specified, using %s"
                    % default_output_format)
        return default_output_format

    # otherwise make sure valid output format is given
    else:
        f_arg_loc = sys.argv.index('-f')

        # check for -f with no argument
        try:
            format_arg = sys.argv[f_arg_loc + 1]
        except IndexError:
            logger.error("-f specified but no argument supplied")

        # check for -f with invalid argument
        if format_arg in valid_baseline_formats:
            return format_arg

        else:
            logger.error("Supplied format arg %s not in %s"
                         % (format_arg, str(valid_baseline_formats)))
    return None


def init_logger():
    logger.handlers = []
    log_level = logging.INFO
    log_format_string = "[%(levelname)7s ] %(message)s"
    logging.captureWarnings(True)
    logger.setLevel(log_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(log_format_string))
    logger.addHandler(handler)


def valid_requirements():
    valid = True

    parser = argparse.ArgumentParser(
        description='Bandit Baseline - Generates Bandit results compared to "'
                    'a baseline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Additional Bandit arguments such as severity filtering (-ll) '
               'can be added and will be passed to Bandit.'
    )

    parser.add_argument('targets', metavar='targets', type=str, nargs='+',
                        help='source file(s) or directory(s) to be tested')

    parser.add_argument('-f', dest='output_format', action='store',
                        default='terminal', help='specify output format',
                        choices=valid_baseline_formats)

    args, unknown = parser.parse_known_args()

    # check valid git project and git installed
    (return_code, _, _) = call_command(['git', 'diff-files', '--quiet',
                                        '--ignore-submodules'])

    if return_code:
        valid = False

        if return_code == 1:
            logger.error('Current tree has un-staged commits')

        elif return_code == 127:
            logger.error("Git command not found")

        elif return_code == 128:
            logger.error("Bandit baseline must be called from a git "
                         "project root")

    # if the output format is 'terminal' we're not going to write a file
    # so there's nothing to check
    if args.output_format != 'terminal' and os.path.exists(report_fname):
        logger.error("File %s already exists, aborting" % report_fname)
        valid = False

    if os.path.exists(baseline_tmp_file):
        logger.error("Temporary file %s needs to be removed prior to running",
                     baseline_tmp_file)

    # we must validate -o is not provided, as it will mess up Bandit baseline
    if '-o' in bandit_args:
        logger.error("Bandit baseline must not be called with the -o option")
        valid = False

    return valid


if __name__ == '__main__':
    main()
