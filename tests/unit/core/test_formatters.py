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

import json
import os
import tempfile

import testtools

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
                   'lineno': 50,
                   'linerange': [0, 1]}
        check_name = 'try_except_pass'
        issue_severity = bandit.LOW
        issue_confidence = bandit.HIGH
        issue_text = 'Try, Except, Pass detected.'
        issue = (issue_severity, issue_confidence, issue_text)
        self.manager.b_rs.out_file = tmp_fname
        self.manager.b_rs.add(context, check_name, issue)

        formatters.report_csv(self.manager.b_rs, None, None, None)

        with open(tmp_fname) as f:
            lines = f.readlines()
            header = ('filename,test_name,issue_severity,issue_confidence,'
                      'issue_text,line_number,line_range')
            self.assertEqual(header, lines[0].rstrip())
            expected = '%s,%s,%s,%s,"%s",%d,"%s"' % (tmp_fname,
                                                     check_name,
                                                     issue_severity,
                                                     issue_confidence,
                                                     issue_text,
                                                     context['lineno'],
                                                     context['linerange'])
            self.assertEqual(expected, lines[1].rstrip())

    def test_report_json(self):
        (tmp_fd, tmp_fname) = tempfile.mkstemp()
        context = {'filename': tmp_fname,
                   'lineno': 50,
                   'linerange': [0, 1]}
        check_name = 'try_except_pass'
        issue_severity = bandit.LOW
        issue_confidence = bandit.HIGH
        issue_text = 'Try, Except, Pass detected.'
        issue = (issue_severity, issue_confidence, issue_text)
        self.manager.b_rs.out_file = tmp_fname
        self.manager.b_rs.add(context, check_name, issue)
        file_list = ['foo.py']
        scores = [{'SEVERITY': [0] * len(constants.RANKING),
                   'CONFIDENCE': [0] * len(constants.RANKING)}]

        formatters.report_json(self.manager.b_rs, file_list, scores, None)

        with open(tmp_fname) as f:
            data = json.loads(f.read())
            self.assertIsNotNone(data['generated_at'])
            self.assertEqual(tmp_fname, data['results'][0]['filename'])
            self.assertEqual(bandit.LOW, data['results'][0]['issue_severity'])
            self.assertEqual(bandit.HIGH,
                             data['results'][0]['issue_confidence'])
            self.assertEqual(issue_text, data['results'][0]['issue_text'])
            self.assertEqual(context['lineno'],
                             data['results'][0]['line_number'])
            self.assertEqual(context['linerange'],
                             data['results'][0]['line_range'])
            self.assertEqual(check_name, data['results'][0]['test_name'])
            self.assertEqual('foo.py', data['stats'][0]['filename'])
            self.assertEqual(0, data['stats'][0]['score'])

    def test_report_text(self):
        (tmp_fd, tmp_fname) = tempfile.mkstemp()
        context = {'filename': tmp_fname,
                   'lineno': 50,
                   'linerange': [0, 1]}
        check_name = 'try_except_pass'
        issue_severity = bandit.LOW
        issue_confidence = bandit.HIGH
        issue_text = 'Try, Except, Pass detected.'
        issue = (issue_severity, issue_confidence, issue_text)
        self.manager.b_rs.out_file = tmp_fname
        self.manager.b_rs.format = 'plain'
        self.manager.b_rs.add(context, check_name, issue)
        file_list = ['foo.py']
        scores = [{'SEVERITY': [0] * len(constants.RANKING),
                   'CONFIDENCE': [0] * len(constants.RANKING)}]
        exc_files = ['test.py']

        formatters.report_text(self.manager.b_rs, file_list, scores, exc_files)

    def test_report_xml(self):
        pass
