# -*- coding:utf-8 -*-
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
import collections
import csv
import datetime
import json
from operator import itemgetter

import six

from bandit.core import constants


def _sum_scores(manager, sev):
    summation = 0
    for scores in manager.scores:
        summation = summation + sum(scores['CONFIDENCE'][sev:])
        summation = summation + sum(scores['SEVERITY'][sev:])
    return summation


def report_csv(manager, filename, sev_level, conf_level, lines, out_format):
    '''Prints/returns warnings in JSON format

    :param result_store: results of scan as BanditResultStore object
    :param files_list: Which files were inspected
    :param scores: The scores awarded to each file in the scope
    :param excluded_files: Which files were excluded from the scope
    :return: A collection containing the CSV data
    '''

    results = manager.get_issue_list()

    if filename is None:
        filename = 'bandit_results.csv'

    with open(filename, 'w') as fout:
        fieldnames = ['filename',
                      'test_name',
                      'issue_severity',
                      'issue_confidence',
                      'issue_text',
                      'line_number',
                      'line_range']

        writer = csv.DictWriter(fout, fieldnames=fieldnames,
                                extrasaction='ignore')
        writer.writeheader()
        for result in results:
            rank = constants.RANKING
            if result.filter(rank[sev_level], rank[conf_level]):
                writer.writerow(result.as_dict(with_code=False))

    print("CSV output written to file: %s" % filename)


def report_json(manager, filename, sev_level, conf_level, lines, out_format):
    '''Prints/returns warnings in JSON format

    :param result_store: results of scan as BanditResultStore object
    :param files_list: Which files were inspected
    :param scores: The scores awarded to each file in the scope
    :param excluded_files: Which files were excluded from the scope
    :return: JSON string
    '''

    stats = dict(zip(manager.files_list, manager.scores))
    machine_output = dict({'results': [], 'errors': [], 'stats': []})
    for (fname, reason) in manager.skipped:
        machine_output['errors'].append({'filename': fname,
                                         'reason': reason})

    for filer, score in six.iteritems(stats):
        totals = {}
        for i in range(sev_level, len(constants.RANKING)):
            severity = constants.RANKING[i]
            severity_value = constants.RANKING_VALUES[severity]
            try:
                sc = score['SEVERITY'][i] / severity_value
            except ZeroDivisionError:
                sc = 0
            totals[severity] = sc

        machine_output['stats'].append({
            'filename': filer,
            'score': _sum_scores(manager, sev_level),
            'issue totals': totals})

    results = manager.get_issue_list()
    collector = []
    for result in results:
        rank = constants.RANKING
        if result.filter(rank[sev_level], rank[conf_level]):
            collector.append(result.as_dict())

    if manager.agg_type == 'vuln':
        machine_output['results'] = sorted(collector,
                                           key=itemgetter('test_name'))
    else:
        machine_output['results'] = sorted(collector,
                                           key=itemgetter('filename'))

    # timezone agnostic format
    TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    time_string = datetime.datetime.utcnow().strftime(TS_FORMAT)
    machine_output['generated_at'] = time_string

    result = json.dumps(machine_output, sort_keys=True,
                        indent=2, separators=(',', ': '))

    if filename:
        with open(filename, 'w') as fout:
            fout.write(result)
        manager.logger.info("JSON output written to file: %s" % filename)
    else:
        print(result)


def report_text(manager, filename, sev_level, conf_level, lines, out_format):
    '''Prints the contents of the result store

    :param result_store: results of scan as BanditResultStore object
    :param files_list: Which files were inspected
    :param scores: The scores awarded to each file in the scope
    :param excluded_files: List of files excluded from the scope
    :return: TXT string with appropriate TTY coloring for terminals
    '''

    tmpstr_list = []

    # use a defaultdict to default to an empty string
    color = collections.defaultdict(str)

    if out_format == 'txt':
        # get text colors from settings for TTY output
        get_setting = manager.b_conf.get_setting
        color = {'HEADER': get_setting('color_HEADER'),
                 'DEFAULT': get_setting('color_DEFAULT'),
                 'LOW': get_setting('color_LOW'),
                 'MEDIUM': get_setting('color_MEDIUM'),
                 'HIGH': get_setting('color_HIGH')
                 }

    # print header
    tmpstr_list.append("%sRun started:%s\n\t%s\n" % (
        color['HEADER'],
        color['DEFAULT'],
        datetime.datetime.utcnow()
    ))

    if manager.verbose:
        # print which files were inspected
        tmpstr_list.append("\n%sFiles in scope (%s):%s\n" % (
            color['HEADER'], len(manager.files_list),
            color['DEFAULT']
        ))

        for item in zip(manager.files_list, map(_sum_scores, manager.scores)):
            tmpstr_list.append("\t%s (score: %i)\n" % item)

        # print which files were excluded and why
        tmpstr_list.append("\n%sFiles excluded (%s):%s\n" %
                           (color['HEADER'], len(manager.skipped),
                            color['DEFAULT']))
        for fname in manager.skipped:
            tmpstr_list.append("\t%s\n" % fname)

    # print which files were skipped and why
    tmpstr_list.append("\n%sFiles skipped (%s):%s\n" % (
        color['HEADER'], len(manager.skipped),
        color['DEFAULT']
    ))

    for (fname, reason) in manager.skipped:
        tmpstr_list.append("\t%s (%s)\n" % (fname, reason))

    # print the results
    tmpstr_list.append("\n%sTest results:%s\n" % (
        color['HEADER'], color['DEFAULT']
    ))

    issues = manager.get_issue_list()
    if not len(issues):
        tmpstr_list.append("\tNo issues identified.\n")

    for issue in issues:
        # if the result isn't filtered out by severity
        rank = constants.RANKING
        if issue.filter(rank[sev_level], rank[conf_level]):
            tmpstr_list.append("\n%s>> Issue: %s\n" % (
                color.get(issue.severity, color['DEFAULT']),
                issue.text
            ))
            tmpstr_list.append("   Severity: %s   Confidence: %s\n" % (
                issue.severity.capitalize(),
                issue.confidence.capitalize()
            ))
            tmpstr_list.append("   Location: %s:%s\n" % (
                issue.fname,
                issue.lineno
            ))
            tmpstr_list.append(color['DEFAULT'])

            tmpstr_list.append(
                issue.get_code(lines, True))

    result = ''.join(tmpstr_list)

    if filename:
        with open(filename, 'w') as fout:
            fout.write(result)
        manager.logger.info("Text output written to file: %s", filename)
    else:
        print(result)


def report_xml(manager, filename, sev_level, conf_level, lines, out_format):
    '''Prints/returns warnings in XML format (Xunit compatible)

    :param result_store: results of scan as BanditResultStore object
    :param files_list: Which files were inspected
    :param scores: The scores awarded to each file in the scope
    :param excluded_files: Which files were excluded from the scope
    :return: A collection containing the XML data
    '''

    import xml.etree.cElementTree as ET

    if filename is None:
        filename = 'bandit_results.xml'

    issues = manager.get_issue_list()
    root = ET.Element('testsuite', name='bandit', tests=str(len(issues)))

    for issue in issues:
        test = issue.test
        testcase = ET.SubElement(root, 'testcase',
                                 classname=issue.fname, name=test)
        rank = constants.RANKING
        if issue.filter(rank[sev_level], rank[conf_level]):
            text = 'Severity: %s Confidence: %s\n%s\nLocation %s:%s'
            text = text % (
                issue.severity, issue.confidence,
                issue.text, issue.fname, issue.lineno)
            ET.SubElement(testcase, 'error',
                          type=issue.severity,
                          message=issue.text).text = text

    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)

    print("XML output written to file: %s" % filename)
