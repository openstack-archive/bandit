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

from collections import OrderedDict
from datetime import datetime
import json
import linecache
from operator import itemgetter
import re
from sys import stdout

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
        filename, lineno = context['filename'], context['lineno']
        (issue_type, issue_text) = issue

        # XXX: tuple usage is fragile because ordering changes on agg_type;
        # ordering is important for reporting as seen in report_json()
        if self.agg_type == 'vuln':
            if test in self.resstore:
                self.resstore[test].append((filename, lineno, issue_type,
                                            issue_text))
            else:
                self.resstore[test] = [(filename, lineno, issue_type,
                                        issue_text)]
        else:
            if filename in self.resstore:
                self.resstore[filename].append((lineno, test, issue_type,
                                                issue_text))
            else:
                self.resstore[filename] = [(lineno, test, issue_type,
                                            issue_text)]
        self.count += 1

    def report_json(self, output_filename=None, stats=None):
        '''Prints/returns warnings in JSON format

        :param output_filename: File to output the results (optional)
        :param stats: dictionary of stats for each file
        :return: JSON string
        '''
        machine_output = dict({'results': [], 'errors': [], 'stats': []})
        collector = list()
        for (fname, reason) in self.skipped:
            machine_output['errors'].append({'filename': fname,
                                            'reason': reason})

        for filer, count in stats.iteritems():
            machine_output['stats'].append({'filename': filer,
                                            'warning_count': count})

        # array indicies are determined by order of tuples defined in add()
        if self.agg_type == 'file':
            for item in self.resstore.items():
                filename = item[0]
                filelist = item[1]
                for x in filelist:
                    holder = dict({"filename": filename,
                                   "line_num": str(x[0]),
                                   "error_label": str(x[1]).strip(),
                                   "error_type": str(x[2]).strip(),
                                   "reason": str(x[3]).strip()})
                    collector.append(holder)
        else:
            for item in self.resstore.items():
                vuln_label = item[0]
                filelist = item[1]
                for x in filelist:
                    holder = dict({"filename": str(x[0]),
                                   "line_num": str(x[1]),
                                   "error_label": vuln_label.strip(),
                                   "error_type": str(x[2]).strip(),
                                   "reason": str(x[3]).strip()})
                    collector.append(holder)

        if self.agg_type == 'vuln':
            machine_output['results'] = sorted(collector,
                                               key=itemgetter('error_type'))
        else:
            machine_output['results'] = sorted(collector,
                                               key=itemgetter('filename'))

        json_output = json.dumps(machine_output, sort_keys=True,
                                 indent=2, separators=(',', ': '))

        # allow disabling of output file if just want JSON object
        if output_filename:
            with open(output_filename, 'w+') as fout:
                fout.write(json_output)
                print("Output written to file: %s" % output_filename)

        return json_output

    def report(self, scope, scores, lines=0, level=1, output_filename=None,
               output_filetype=None):
        '''Prints the contents of the result store

        :param scope: Which files were inspected
        :param scores: The scores awarded to each file in the scope
        :param lines: # of lines around the issue line to display (optional)
        :param level: What level of severity to display (optional)
        :param output_filename: File to output the results (optional)
        :param output_filetype: File type to output
        :return: -
        '''

        # display output using colors if not writing to a file
        is_tty = False if output_filename is not None else stdout.isatty()

        scores_dict = dict(zip(scope, scores))
        if output_filetype == 'json' and not output_filename:
            return self.report_json('results.json', scores_dict)
        elif output_filetype == 'json':
            return self.report_json(output_filename, scores_dict)

        if level >= len(constants.SEVERITY):
            level = len(constants.SEVERITY) - 1

        tmpstr = ""

        # get text colors from settings
        color = dict()
        color['HEADER'] = self.config.get_setting('color_HEADER')
        color['DEFAULT'] = self.config.get_setting('color_DEFAULT')
        color['INFO'] = self.config.get_setting('color_INFO')
        color['WARN'] = self.config.get_setting('color_WARN')
        color['ERROR'] = self.config.get_setting('color_ERROR')

        # print header
        if is_tty:
            tmpstr += "%sRun started:%s\n\t%s\n" % (
                color['HEADER'],
                color['DEFAULT'],
                datetime.utcnow()
            )
        else:
            tmpstr += "Run started:\n\t%s\n" % datetime.utcnow()

        # print which files were inspected
        if is_tty:
            tmpstr += "%sFiles in scope (%s):%s\n" % (
                color['HEADER'], len(scope),
                color['DEFAULT']
            )
        else:
            tmpstr += "Files in scope (%s):\n" % (len(scope))

        for item in zip(scope, scores):
            tmpstr += "\t%s (score: %i)\n" % item

        # print which files were skipped and why
        if is_tty:
            tmpstr += "%sFiles skipped (%s):%s" % (
                color['HEADER'], len(self.skipped),
                color['DEFAULT']
            )
        else:
            tmpstr += "Files skipped (%s):" % len(self.skipped)

        for (fname, reason) in self.skipped:
            tmpstr += "\n\t%s (%s)" % (fname, reason)

        # print the results
        if is_tty:
            tmpstr += "\n%sTest results:%s\n" % (
                color['HEADER'], color['DEFAULT']
            )
        else:
            tmpstr += "\nTest results:\n"

        if self.count == 0:
            tmpstr += "\tNo issues identified.\n"
        # if aggregating by vulnerability type
        elif self.agg_type == 'vuln':
            for test, issues in self.resstore.items():
                for filename, lineno, issue_type, issue_text in issues:
                    issue_line = linecache.getline(filename, lineno)
                    # if the line doesn't have one of the skip tags, keep going
                    if re.search(constants.SKIP_RE, issue_line):
                        continue
                    # if the result in't filtered out by severity
                    if constants.SEVERITY.index(issue_type) >= level:
                        if is_tty:
                            tmpstr += "%s>> %s\n - %s::%s%s\n" % (
                                color.get(issue_type, color['DEFAULT']),
                                issue_text, filename, lineno,
                                color['DEFAULT']
                            )
                        else:
                            tmpstr += ">> %s\n - %s::%s\n" % (
                                issue_text, filename, lineno
                            )

                        for i in utils.mid_range(lineno, lines):
                            line = linecache.getline(filename, i)
                            # linecache returns '' if line does not exist
                            if line != '':
                                tmpstr += "\t%3d  %s" % (
                                    i, linecache.getline(filename, i)
                                )
        # otherwise, aggregating by filename
        else:
            for filename, issues in self.resstore.items():
                for lineno, test, issue_type, issue_text in issues:
                    issue_line = linecache.getline(filename, lineno)
                    # if the line doesn't have one of the skip tags, keep going
                    if re.search(constants.SKIP_RE, issue_line):
                        continue
                    # if the result isn't filtered out by severity
                    if constants.SEVERITY.index(issue_type) >= level:
                        if is_tty:
                            tmpstr += "%s>> %s\n - %s::%s%s\n" % (
                                color.get(
                                    issue_type, color['DEFAULT']
                                ),
                                issue_text, filename, lineno,
                                color['DEFAULT']
                            )
                        else:
                            tmpstr += ">> %s\n - %s::%s\n" % (
                                issue_text, filename, lineno
                            )
                        for i in utils.mid_range(lineno, lines):
                            line = linecache.getline(filename, i)
                            # linecache returns '' if line does not exist
                            if line != '':
                                tmpstr += "\t%3d  %s" % (
                                    i, linecache.getline(filename, i)
                                )
        # output to a file,
        if output_filename is not None:
            with open(output_filename, 'w') as fout:
                fout.write(tmpstr)
            print("Output written to file: %s" % output_filename)
        # or print the results on screen
        else:
            print(tmpstr)
