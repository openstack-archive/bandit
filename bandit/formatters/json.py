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

from __future__ import absolute_import
import datetime
import json
import logging
from operator import itemgetter

import six

from bandit.core import constants
from bandit.core import utils

logger = logging.getLogger(__name__)


def report(manager, filename, sev_level, conf_level, lines=-1,
           out_format='json'):
    '''''Prints issues in JSON format

    :param manager: the bandit manager object
    :param filename: The output file name, or None for stdout
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param lines: Number of lines to report, -1 for all
    :param out_format: The ouput format name
    '''

    stats = dict(zip(manager.files_list, manager.scores))
    machine_output = dict({'results': [], 'errors': [], 'stats': []})
    for (fname, reason) in manager.skipped:
        machine_output['errors'].append({'filename': fname,
                                         'reason': reason})

    for filer, score in six.iteritems(stats):
        totals = {}
        rank = constants.RANKING
        sev_idx = rank.index(sev_level)
        for i in range(sev_idx, len(rank)):
            severity = rank[i]
            severity_value = constants.RANKING_VALUES[severity]
            try:
                sc = score['SEVERITY'][i] / severity_value
            except ZeroDivisionError:
                sc = 0
            totals[severity] = sc

        machine_output['stats'].append({
            'filename': filer,
            'score': utils.sum_scores(manager, sev_idx),
            'issue totals': totals})

    results = manager.get_issue_list()
    collector = []
    for result in results:
        if result.filter(sev_level, conf_level):
            collector.append(result.as_dict())

    if manager.agg_type == 'vuln':
        machine_output['results'] = sorted(collector,
                                           key=itemgetter('test_name'))
    else:
        machine_output['results'] = sorted(collector,
                                           key=itemgetter('filename'))

    machine_output['metrics'] = manager.metrics

    # timezone agnostic format
    TS_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    time_string = datetime.datetime.utcnow().strftime(TS_FORMAT)
    machine_output['generated_at'] = time_string

    result = json.dumps(machine_output, sort_keys=True,
                        indent=2, separators=(',', ': '))

    if filename:
        with open(filename, 'w') as fout:
            fout.write(result)
        logger.info("JSON output written to file: %s" % filename)
    else:
        print(result)
