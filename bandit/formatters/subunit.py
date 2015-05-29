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

from __future__ import absolute_import

import functools
import sys

import subunit


def _write_subunit_result(self, output, status, name, metadata=None,
                          attachments=None):
    partial = functools.partial
    STATUS_CODES = frozenset([
        'exists',
        'fail',
        'skip',
        'success',
        'uxsuccess',
        'xfail',
    ])
    if metadata is None:
        metadata = {}
    write_status = output.status
    tags = metadata.get('tags')
    if 'tags' is not None:
        write_status = partial(write_status, test_tags=tags.split(','))
    write_status = partial(write_status, test_id=name)
    write_status()
    write_status = partial(write_status, test_id=name)
    if status in STATUS_CODES:
        write_status = partial(write_status, test_status=status)
    write_status()
    if attachments:
        for attach in attachments:
            write_status = partial(write_status, filename=attach,
                                   file_bytes=attachments[attach], eof=True)
    write_status()


def report(manager, filename, sev_level, conf_level, lines=-1,
           out_format='subunit'):
    """Prints/returns warnings in subunit format

    For more information on the subunit protocol see the official
    documentation:

    https://github.com/testing-cabal/subunit#the-protocol

    :param manager: the bandit manager object
    :param filename: The output file name, or None for stdout
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param lines: Number of lines to report, -1 for all
    :param out_format: The ouput format name
    """
    results = manager.get_issue_list()
    if filename is None:
        output = sys.stdout
    else:
        output = open(filename, 'w')

    output = subunit.v2.StreamResultToBytes(output)
    output.startTestRun()

    for result in results:
        if result.filter(sev_level, conf_level):
            issue = result.as_dict(with_code=False)
            test = issue['test_name']
            fname = issue['fname']
            name = fname + '[' + test + ']'
            text = 'Severity: %s Confidence: %s\n%s\nLocation %s:%s'
            text = text % (
                issue['issue_severity'], issue['issue_confidence'],
                issue['issue_text'], issue['fname'], issue['lineno'])
            attachments = {'issue': text}
            _write_subunit_result(output, 'fail', name,
                                  attachments=attachments)
    output.stopTestRun()
