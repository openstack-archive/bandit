# Copyright (c) 2017 Hewlett Packard Enterprise
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

r"""
================
Custom Formatter
================

This formatter outputs the issues in custom machine-readable format.

default template: <abspath>:<line>: <test_id>[bandit]: <severity>: <msg>

:Example:

/usr/lib/python3.6/site-packages/openlp/core/utils/__init__.py: \
405: B310[bandit]: MEDIUM: Audit url open for permitted schemes. \
Allowing use of file:/ or custom schemes is often unexpected.

"""

import logging
import os
import re
import sys

from bandit.core import test_properties

LOG = logging.getLogger(__name__)


@test_properties.accepts_baseline
def report(manager, fileobj, sev_level, conf_level, lines=-1, template=None):
    """Prints issues in custom format

    :param manager: the bandit manager object
    :param fileobj: The output file object, which may be sys.stdout
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param lines: Number of lines to report, -1 for all
    :param template: Output template with non-terminal tags <N>
                    (default: <abspath>:<line>:
                     <test_id>[bandit]: <severity>: <msg>)
    """

    machine_output = {'results': [], 'errors': []}
    for (fname, reason) in manager.get_skipped():
        machine_output['errors'].append({'filename': fname,
                                         'reason': reason})

    results = manager.get_issue_list(sev_level=sev_level,
                                     conf_level=conf_level)

    msg_template = template
    if template is None:
        msg_template = "<abspath>:<line>: <test_id>[bandit]: <severity>: <msg>"

    # Dictionary of non-terminal tags that will be expanded
    non_terminals = {
        '<abspath>': lambda issue: os.path.abspath(issue.fname),
        '<relpath>': lambda issue: os.path.relpath(issue.fname),
        '<line>': lambda issue: issue.lineno,
        '<test_id>': lambda issue: issue.test_id,
        '<severity>': lambda issue: issue.severity,
        '<msg>': lambda issue: issue.text,
        '<confidence>': lambda issue: issue.confidence,
        '<range>': lambda issue: issue.linerange
    }

    output = ""
    pattern = re.compile("<[^>]*>")
    # Substitute non terminal characters
    msg_template_sub = re.sub(pattern, "{}", msg_template)
    msg_template_sub += "\n"

    limit = lines if lines > 0 else None
    for defect in results[:limit]:
        # Substitute non terminal symbols in msg_template
        sub_result = []
        for tag in re.findall(pattern, msg_template):
            if tag in non_terminals.keys():
                sub_result.append(non_terminals[tag](defect))
            else:
                LOG.warning(
                    "  Tag %s was not recognized and will not be expanded", tag
                )
                sub_result.append(tag)

        output += msg_template_sub.format(*sub_result)

    with fileobj:
        fileobj.write(output)

    if fileobj.name != sys.stdout.name:
        LOG.info("Machine output written to file: %s", fileobj.name)
