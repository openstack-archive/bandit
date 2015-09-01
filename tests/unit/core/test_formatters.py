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
        (tmp_fd, self.tmp_fname) = tempfile.mkstemp()
        self.context = {'filename': self.tmp_fname,
                        'lineno': 4,
                        'linerange': [4]}
        self.check_name = 'hardcoded_bind_all_interfaces'
        self.issue = (bandit.MEDIUM, bandit.MEDIUM,
                      'Possible binding to all interfaces.')
        self.manager.b_rs.out_file = self.tmp_fname
        self.manager.b_rs.add(self.context, self.check_name, self.issue)

    def test_report_csv(self):
        formatters.report_csv(self.manager.b_rs, None, None, None)

        with open(self.tmp_fname) as f:
            reader = csv.DictReader(f)
            data = six.next(reader)
            self.assertEqual(self.tmp_fname, data['filename'])
            self.assertEqual(self.issue[0], data['issue_severity'])
            self.assertEqual(self.issue[1], data['issue_confidence'])
            self.assertEqual(self.issue[2], data['issue_text'])
            self.assertEqual(six.text_type(self.context['lineno']),
                             data['line_number'])
            self.assertEqual(six.text_type(self.context['linerange']),
                             data['line_range'])
            self.assertEqual(self.check_name, data['test_name'])

    def test_report_json(self):
        file_list = ['binding.py']
        scores = [{'SEVERITY': [0] * len(constants.RANKING),
                   'CONFIDENCE': [0] * len(constants.RANKING)}]

        formatters.report_json(self.manager.b_rs, file_list, scores, None)

        with open(self.tmp_fname) as f:
            data = json.loads(f.read())
            self.assertIsNotNone(data['generated_at'])
            self.assertEqual(self.tmp_fname, data['results'][0]['filename'])
            self.assertEqual(self.issue[0], data['results'][0]['issue_severity'])
            self.assertEqual(self.issue[1],
                             data['results'][0]['issue_confidence'])
            self.assertEqual(self.issue[2], data['results'][0]['issue_text'])
            self.assertEqual(self.context['lineno'],
                             data['results'][0]['line_number'])
            self.assertEqual(self.context['linerange'],
                             data['results'][0]['line_range'])
            self.assertEqual(self.check_name, data['results'][0]['test_name'])
            self.assertEqual('binding.py', data['stats'][0]['filename'])
            self.assertEqual(0, data['stats'][0]['score'])

    def test_report_text(self):
        self.manager.b_rs.format = 'txt'
        self.manager.b_rs.verbose = True
        file_list = ['binding.py']
        scores = [{'SEVERITY': [0] * len(constants.RANKING),
                   'CONFIDENCE': [0] * len(constants.RANKING)}]
        exc_files = ['test_binding.py']

        formatters.report_text(self.manager.b_rs, file_list, scores, exc_files)

        with open(self.tmp_fname) as f:
            data = f.read()
            expected = '>> Issue: %s' % self.issue[2]
            self.assertIn(expected, data)
            expected = '   Severity: %s   Confidence: %s' % (
                self.issue[0].capitalize(), self.issue[1].capitalize())
            self.assertIn(expected, data)
            expected = '   Location: %s:%d' % (self.tmp_fname, self.context['lineno'])
            self.assertIn(expected, data)

    def test_report_xml(self):
        formatters.report_xml(self.manager.b_rs, None, None, None)

        with open(self.tmp_fname) as f:
            data = xmltodict.parse(f.read())
            self.assertEqual(self.tmp_fname,
                data['testsuite']['testcase']['@classname'])
            self.assertEqual(self.issue[2],
                data['testsuite']['testcase']['error']['@message'])
            self.assertEqual(self.check_name,
                data['testsuite']['testcase']['@name'])
