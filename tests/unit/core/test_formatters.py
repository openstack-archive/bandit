# Copyright (c) 2015 VMware, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import csv
import json
import os
import tempfile

import six
import testtools
import xmltodict

import bandit
from bandit.core import constants
from bandit.core import manager
from bandit.core import formatters


class FormattersTests(testtools.TestCase):

    def setUp(self):
        super(FormattersTests, self).setUp()
        cfg_file = os.path.join(os.getcwd(), 'bandit/config/bandit.yaml')
        path = os.path.join(os.getcwd(), 'bandit', 'plugins')
        self.manager = manager.BanditManager(cfg_file, 'file')

    def test_report_csv(self):
        (tmp_fd, tmp_fname) = tempfile.mkstemp()
        context = {'filename': tmp_fname,
                   'lineno': 4,
                   'linerange': [4]}
        check_name = 'hardcoded_bind_all_interfaces'
        issue_severity = bandit.MEDIUM
        issue_confidence = bandit.MEDIUM
        issue_text = 'Possible binding to all interfaces.'
        issue = (issue_severity, issue_confidence, issue_text)
        self.manager.b_rs.out_file = tmp_fname
        self.manager.b_rs.add(context, check_name, issue)

        formatters.report_csv(self.manager.b_rs, None, None, None)

        with open(tmp_fname) as f:
            reader = csv.DictReader(f)
            data = reader.next()
            self.assertEqual(tmp_fname, data['filename'])
            self.assertEqual(bandit.MEDIUM, data['issue_severity'])
            self.assertEqual(bandit.MEDIUM, data['issue_confidence'])
            self.assertEqual(issue_text, data['issue_text'])
            self.assertEqual(six.text_type(context['lineno']),
                             data['line_number'])
            self.assertEqual(six.text_type(context['linerange']),
                             data['line_range'])
            self.assertEqual(check_name, data['test_name'])

    def test_report_json(self):
        (tmp_fd, tmp_fname) = tempfile.mkstemp()
        context = {'filename': tmp_fname,
                   'lineno': 4,
                   'linerange': [4]}
        check_name = 'hardcoded_bind_all_interfaces'
        issue_severity = bandit.MEDIUM
        issue_confidence = bandit.MEDIUM
        issue_text = 'Possible binding to all interfaces.'
        issue = (issue_severity, issue_confidence, issue_text)
        self.manager.b_rs.out_file = tmp_fname
        self.manager.b_rs.add(context, check_name, issue)
        file_list = ['binding.py']
        scores = [{'SEVERITY': [0] * len(constants.RANKING),
                   'CONFIDENCE': [0] * len(constants.RANKING)}]

        formatters.report_json(self.manager.b_rs, file_list, scores, None)

        with open(tmp_fname) as f:
            data = json.loads(f.read())
            self.assertIsNotNone(data['generated_at'])
            self.assertEqual(tmp_fname, data['results'][0]['filename'])
            self.assertEqual(bandit.MEDIUM, data['results'][0]['issue_severity'])
            self.assertEqual(bandit.MEDIUM,
                             data['results'][0]['issue_confidence'])
            self.assertEqual(issue_text, data['results'][0]['issue_text'])
            self.assertEqual(context['lineno'],
                             data['results'][0]['line_number'])
            self.assertEqual(context['linerange'],
                             data['results'][0]['line_range'])
            self.assertEqual(check_name, data['results'][0]['test_name'])
            self.assertEqual('binding.py', data['stats'][0]['filename'])
            self.assertEqual(0, data['stats'][0]['score'])

    def test_report_text(self):
        (tmp_fd, tmp_fname) = tempfile.mkstemp()
        context = {'filename': tmp_fname,
                   'lineno': 4,
                   'linerange': [4]}
        check_name = 'hardcoded_bind_all_interfaces'
        issue_severity = bandit.MEDIUM
        issue_confidence = bandit.MEDIUM
        issue_text = 'Possible binding to all interfaces.'
        issue = (issue_severity, issue_confidence, issue_text)
        self.manager.b_rs.out_file = tmp_fname
        self.manager.b_rs.format = 'txt'
        self.manager.b_rs.verbose = True
        self.manager.b_rs.add(context, check_name, issue)
        file_list = ['binding.py']
        scores = [{'SEVERITY': [0] * len(constants.RANKING),
                   'CONFIDENCE': [0] * len(constants.RANKING)}]
        exc_files = ['test_binding.py']

        formatters.report_text(self.manager.b_rs, file_list, scores, exc_files)

        with open(tmp_fname) as f:
            data = f.read()
            expected = '>> Issue: %s' % issue_text
            self.assertIn(expected, data)
            expected = '   Severity: %s   Confidence: %s' % (
                issue_severity.capitalize(), issue_confidence.capitalize())
            self.assertIn(expected, data)
            expected = '   Location: %s:%d' % (tmp_fname, context['lineno'])
            self.assertIn(expected, data)

    def test_report_xml(self):
        (tmp_fd, tmp_fname) = tempfile.mkstemp()
        context = {'filename': tmp_fname,
                   'lineno': 4,
                   'linerange': [4]}
        check_name = 'hardcoded_bind_all_interfaces'
        issue_severity = bandit.MEDIUM
        issue_confidence = bandit.MEDIUM
        issue_text = 'Possible binding to all interfaces.'
        issue = (issue_severity, issue_confidence, issue_text)
        self.manager.b_rs.out_file = tmp_fname
        self.manager.b_rs.add(context, check_name, issue)
        file_list = ['binding.py']
        scores = [{'SEVERITY': [0] * len(constants.RANKING),
                   'CONFIDENCE': [0] * len(constants.RANKING)}]

        formatters.report_xml(self.manager.b_rs, None, None, None)

        with open(tmp_fname) as f:
            data = xmltodict.parse(f.read())
            self.assertEqual(tmp_fname,
                data['testsuite']['testcase']['@classname'])
            self.assertEqual(issue_text,
                data['testsuite']['testcase']['error']['@message'])
            self.assertEqual(check_name,
                data['testsuite']['testcase']['@name'])
