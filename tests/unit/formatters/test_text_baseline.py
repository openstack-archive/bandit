# Copyright (c) 2015 Hewlett Packard Enterprise
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
import mock
import tempfile

import testtools

import bandit
from bandit.core import constants
from bandit.core import config
from bandit.core import manager
from bandit.core import metrics
from bandit.core import issue
from bandit.formatters import text_baseline as b_text

class TextBaselineFormatterTests(testtools.TestCase):

    def setUp(self):
        super(TextBaselineFormatterTests, self).setUp()

    @mock.patch('bandit.core.issue.Issue.get_code')
    def test_output_issue(self, get_code):
        issue = _get_issue_instance()
        get_code.return_value = 'DDDDDDD'
        color = {'MEDIUM': 'AAAAAAA',
                 'DEFAULT': 'BBBBBBB'}

        indent_val = 'CCCCCCC'

        def _template(_issue, _color, _indent_val, _code):
            return_val = ["\n{}{}>> Issue: [{}] {}\n".
                          format(_indent_val, _color['MEDIUM'], _issue.test,
                                 _issue.text),
                          "{}   Severity: {}   Confidence: {}\n".
                          format(_indent_val, _issue.severity.capitalize(),
                                 _issue.confidence.capitalize()),
                          "{}   Location: {}:{}\n".
                          format(_indent_val, _issue.fname, _issue.lineno),
                          "{}".format(_color['DEFAULT'])]
            if _code:
                return_val.append("{}{}\n".format(_indent_val, _code))
            return return_val

        issue_text = b_text._output_issue_str(issue, color, indent_val)
        expected_return = _template(issue, color, indent_val, 'DDDDDDD')
        self.assertEqual(expected_return, issue_text)

        issue_text = b_text._output_issue_str(issue, color, indent_val,
                                              show_code=False)
        expected_return = _template(issue, color, indent_val, '')
        self.assertEqual(expected_return, issue_text)

        issue.lineno = ''
        issue_text = b_text._output_issue_str(issue, color, indent_val,
                                              show_lineno=False)
        expected_return = _template(issue, color, indent_val, 'DDDDDDD')
        self.assertEqual(expected_return, issue_text)

    def test_report(self):
        #TODO(tmcpeak)
        pass


def _get_issue_instance(severity=bandit.MEDIUM, confidence=bandit.MEDIUM):
    new_issue = issue.Issue(severity, confidence, 'Test issue')
    new_issue.fname = 'code.py'
    new_issue.test = 'bandit_plugin'
    new_issue.lineno = 1
    return new_issue
