# -*- coding:utf-8 -*-
#
# Copyright 2014 Hewlett-Packard Development Company, L.P.
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


"""An object to store/access results associated with Bandit tests."""

from collections import defaultdict
from collections import OrderedDict
import csv
from datetime import datetime
import json
import linecache
from operator import itemgetter

import constants
import utils


class BanditResultStore():
    resstore = OrderedDict()
    count = 0
    skipped = None

    def __init__(self, logger, config, agg_type):
        self.count = 0
        self.skipped = []
        self.logger = logger
        self.config = config
        self.agg_type = agg_type
        self.level = 0
        self.max_lines = -1
        self.format = 'txt'

    @property
    def count(self):
        '''Count property - used to get the current number of test results

        :return: The current count of test results
        '''
        return self.count

    def skip(self, filename, reason):
        '''Indicates that the specified file was skipped and why

        :param filename: The file that was skipped
        :param reason: Why the file was skipped
        :return: -
        '''
        self.skipped.append((filename, reason))

    def add(self, context, test, issue):
        '''Adds a result, with the context and the issue that was found

        :param context: Context of the node
        :param test: The type (function name) of the test
        :param issue: Which issue was found
        :return: -
        '''
        filename = context['filename']
        lineno = context['lineno']
        linerange = context['statement']['linerange']
        (issue_type, issue_text) = issue

        if self.agg_type == 'vuln':
            key = test
        else:
            key = filename

        self.resstore.setdefault(key, []).append(
            {'fname': filename,
             'test': test,
             'lineno': lineno,
             'linerange': linerange,
             'issue_type': issue_type,
             'issue_text': issue_text})

        self.count += 1

    def _report_csv(self, file_list, scores, excluded_files, output_filename):
        '''Prints/returns warnings in JSON format

        :param files_list: Which files were inspected
        :param scores: The scores awarded to each file in the scope
        :param excluded_files: Which files were excluded from the scope
        :return: A collection containing the CSV data
        '''

        results = self._get_issue_list()

        # Remove the code from all the issues in the list, as we will not
        # be including it in the CSV data.
        def del_code(issue):
            del issue['code']
        map(del_code, results)

        if output_filename is None:
            output_filename = 'bandit_results.csv'

        try:
            with open(output_filename, 'w') as fout:
                fieldnames = ['filename',
                              'error_type',
                              'error_label',
                              'line_num',
                              'reason',
                              'line_range']

                writer = csv.DictWriter(fout, fieldnames=fieldnames)
                writer.writeheader()
                for result in results:
                    writer.writerow(result)

            print("CSV output written to file: %s" % output_filename)
        except:
            print("Unable to write to file: %s" % output_filename)


    def _report_json(self, file_list, scores, excluded_files, output_filename):
        '''Prints/returns warnings in JSON format

        :param files_list: Which files were inspected
        :param scores: The scores awarded to each file in the scope
        :param excluded_files: Which files were excluded from the scope
        :return: JSON string
        '''

        stats = dict(zip(file_list, scores))

        machine_output = dict({'results': [], 'errors': [], 'stats': []})
        collector = list()
        for (fname, reason) in self.skipped:
            machine_output['errors'].append({'filename': fname,
                                            'reason': reason})

        for filer, score in stats.iteritems():
            totals = {}
            for i in range(self.level, len(constants.SEVERITY)):
                severity = constants.SEVERITY[i]
                sc = score[i] / constants.SEVERITY_VALUES[severity]
                totals[severity] = sc

            machine_output['stats'].append({'filename': filer,
                                            'score': self._sum_scores(score),
                                            'issue totals': totals})

        collector = self._get_issue_list()

        if self.agg_type == 'vuln':
            machine_output['results'] = sorted(collector,
                                               key=itemgetter('error_type'))
        else:
            machine_output['results'] = sorted(collector,
                                               key=itemgetter('filename'))

        result = json.dumps(machine_output, sort_keys=True,
                            indent=2, separators=(',', ': '))

        if output_filename is not None:
            with open(output_filename, 'w') as fout:
                fout.write(result)
                # XXX: Should this be log output? (ukbelch)
            print("JSON output written to file: %s" % output_filename)
        else:
            print(result)

    def _report_text(self, files_list, scores, excluded_files,
                     output_filename):
        '''Prints the contents of the result store

        :param files_list: Which files were inspected
        :param scores: The scores awarded to each file in the scope
        :param excluded_files: List of files excluded from the scope
        :return: TXT string with appropriate TTY coloring for terminals
        '''

        tmpstr_list = []

        # use a defaultdict to default to an empty string
        color = defaultdict(str)

        if self.format == 'txt':
            # get text colors from settings for TTY output
            get_setting = self.config.get_setting
            color = {'HEADER': get_setting('color_HEADER'),
                     'DEFAULT': get_setting('color_DEFAULT'),
                     'INFO': get_setting('color_INFO'),
                     'WARN': get_setting('color_WARN'),
                     'ERROR': get_setting('color_ERROR')
                     }

        # print header
        tmpstr_list.append("%sRun started:%s\n\t%s\n" % (
            color['HEADER'],
            color['DEFAULT'],
            datetime.utcnow()
        ))

        # print which files were inspected
        tmpstr_list.append("\n%sFiles in scope (%s):%s\n" % (
            color['HEADER'], len(files_list),
            color['DEFAULT']
        ))

        for item in zip(files_list, map(self._sum_scores, scores)):
            tmpstr_list.append("\t%s (score: %i)\n" % item)

        # print which files were excluded and why
        tmpstr_list.append("\n%sFiles excluded (%s):%s\n" % (color['HEADER'],
                           len(excluded_files), color['DEFAULT']))
        for fname in excluded_files:
            tmpstr_list.append("\t%s\n" % fname)

        # print which files were skipped and why
        tmpstr_list.append("\n%sFiles skipped (%s):%s\n" % (
            color['HEADER'], len(self.skipped),
            color['DEFAULT']
        ))

        for (fname, reason) in self.skipped:
            tmpstr_list.append("\t%s (%s)\n" % (fname, reason))

        # print the results
        tmpstr_list.append("\n%sTest results:%s\n" % (
            color['HEADER'], color['DEFAULT']
        ))

        if self.count == 0:
            tmpstr_list.append("\tNo issues identified.\n")

        for key, issues in self.resstore.items():
            for issue in issues:

                # if the result in't filtered out by severity
                if self._check_severity(issue['issue_type']):
                    tmpstr_list.append("\n%s>> %s\n - %s::%s%s\n" % (
                        color.get(issue['issue_type'], color['DEFAULT']),
                        issue['issue_text'],
                        issue['fname'],
                        issue['lineno'],
                        color['DEFAULT']
                    ))

                    tmpstr_list.append(
                        self._get_code(issue, True))

        result = ''.join(tmpstr_list)

        if output_filename is not None:
            with open(output_filename, 'w') as fout:
                fout.write(result)
                # XXX: Should this be log output? (ukbelch)
            print("Text output written to file: %s" % output_filename)
        else:
            print(result)

    def report(self, files_list, scores, excluded_files=None, lines=-1,
               level=1, output_filename=None, output_format=None):
        '''Prints the contents of the result store

        :param scope: Which files were inspected
        :param scores: The scores awarded to each file in the scope
        :param lines: # of lines around the issue line to display (optional)
        :param level: What level of severity to display (optional)
        :param output_filename: File to output the results (optional)
        :param output_format: File type to output (json|txt)
        :return: -
        '''

        if not excluded_files:
            excluded_files = []

        if level >= len(constants.SEVERITY):
            level = len(constants.SEVERITY) - 1

        self.level = level
        self.max_lines = lines
        self.format = output_format

        if self.format == 'json':
            self._report_json(files_list, scores,
                              excluded_files=excluded_files,
                              output_filename=output_filename)

        elif self.format == 'csv':
            self.max_lines = 1
            self._report_csv(files_list, scores,
                             excluded_files=excluded_files,
                             output_filename=output_filename)

        else:
            # format is the default "txt"
            if output_filename:
                # output to file, specify plain text
                self.format = 'plain'
            self._report_text(files_list, scores,
                              excluded_files=excluded_files,
                              output_filename=output_filename)

    def _get_issue_list(self):

        collector = list()

        for group in self.resstore.items():
            issue_list = group[1]
            for issue in issue_list:
                if self._check_severity(issue['issue_type']):
                    code = self._get_code(issue, True)
                    holder = dict({"filename": issue['fname'],
                                   "line_num": issue['lineno'],
                                   "line_range": issue['linerange'],
                                   "error_label": issue['test'],
                                   "error_type": issue['issue_type'],
                                   "code": code,
                                   "reason": issue['issue_text']})
                    collector.append(holder)

        return collector

    def _get_code(self, issue, tabbed=False):
        '''Gets lines of code from a file

        :param filename: Filename of file with code in it
        :param line_list: A list of integers corresponding to line numbers
        :return: string of code
        '''
        issue_line = []
        prepend = ""

        file_len = self._file_length(issue['fname'])
        lines = utils.lines_with_context(issue['lineno'],
                                         issue['linerange'],
                                         self.max_lines,
                                         file_len)

        for l in lines:
            if l:
                if tabbed:
                    prepend = "%s\t" % l
                issue_line.append(prepend + linecache.getline(
                                  issue['fname'],
                                  l))

        return ''.join(issue_line)

    def _file_length(self, filename):
        with open(filename) as f:
            for line, l in enumerate(f):
                pass
        return line + 1

    def _sum_scores(self, score_list):
        '''Get total of all scores

        This just computes the sum of all recorded scores, filtering them
        on the chosen minimum severity level.
        :param score_list: the list of scores to total
        :return: an integer total sum of all scores above the threshold
        '''
        return sum(score_list[self.level:])

    def _check_severity(self, severity):
        '''Check severity level

        returns true if the issue severity is above the threshold.
        :param severity: the severity of the issue being checked
        :return: boolean result
        '''
        return constants.SEVERITY.index(severity) >= self.level
