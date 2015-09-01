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

import os
import tempfile

import testtools

import bandit
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

        self.assertEqual(tmp_fname, self.manager.b_rs.out_file)
        with open(tmp_fname) as f:
            lines = f.readlines()
            self.assertEqual('filename,test_name,issue_severity,'
                             'issue_confidence,issue_text,line_number,'
                             'line_range', lines[0].strip())
            expected = '%s,%s,%s,%s,"%s",%d,"%s"' % (tmp_fname,
                                                 check_name,
                                                 issue_severity,
                                                 issue_confidence,
                                                 issue_text,
                                                 context['lineno'],
                                                 context['linerange'])
            self.assertEqual(expected, lines[1].strip())

    def report_json(self):
        pass

    def report_text(self):
        pass

    def report_xml(self):
        pass
