# Copyright (c) 2015 Rackspace, Inc.
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

import logging

from bandit.core.test_properties import accepts_baseline
from bandit.core import utils

logger = logging.getLogger(__name__)


@accepts_baseline
def report(manager, filename, sev_level, conf_level, lines=-1,
           out_format='html'):
    """Writes issues to 'filename' in HTML format

    :param manager: the bandit manager object
    :param filename: output file name
    :param sev_level: Filtering severity level
    :param conf_level: Filtering confidence level
    :param lines: Number of lines to report, -1 for all
    :param out_format: The output format name
    """

    header_block = """
<!DOCTYPE html>
<html>
<head>

<title>
    Bandit Report
</title>

<style>

html * {
    font-family: "Arial", sans-serif;
}

pre {
    font-family: "Monaco", monospace;
}

.bordered-box {
    border: 1px solid black;
    padding-top:.5em;
    padding-bottom:.5em;
    padding-left:1em;

}

.metrics-box {
    font-size: 1.1em;
    line-height: 130%;
}

.metrics-title {
    font-size: 1.5em;
    font-weight: 500;
    margin-bottom: .25em;
}

.issue-description {
    font-size: 1.3em;
    font-weight: 500;
}

.candidate-issues {
    margin-left: 2em;
    border-left: solid 1px; LightGray;
    padding-left: 5%;
    margin-top: .2em;
    margin-bottom: .2em;
}

.issue-block {
    border: 1px solid LightGray;
    padding-left: .5em;
    padding-top: .5em;
    padding-bottom: .5em;
    margin-bottom: .5em;
}

.issue-sev-high {
    background-color: Pink;
}

.issue-sev-medium {
    background-color: NavajoWhite;
}

.issue-sev-low {
    background-color: LightCyan;
}

</style>
</head>
    """

    report_block = """
<body>
{metrics}
{skipped}

<br>
<span id='results'>
    {results}
</span>

</body>
</html>
    """

    issue_block = """
<span id='issue-{issue_no}'>
<div class='issue-block {issue_class}'>
    <b>{test_name}: </b> {test_text}<br>
    <b>Severity: </b>{severity}<br />
    <b>Confidence: </b>{confidence}</br />
    <b>File: </b><a href='{path}' target='_blank'>{path}</a> <br />
{code}
{candidates}
</div>
</span>
    """

    code_block = """
<span id='code'>
<pre>
{code}
</pre>
</span>"""

    candidate_block = """
<span id='candidates'>
<br>
<b>Candidates: </b>
{candidate_list}
</span>
    """

    candidate_issue = """
<span id='candidate'>
<div class='candidate-issues'>
<pre>{code}</pre>
</div>
</span>
"""

    skipped_block = """
<br>
<span id='skipped'>
<div class='bordered-box'>
<b>Skipped files:</b><br><br>
{files_list}
</div>
</span>
"""

    metrics_block = """
<span id='metrics'>
    <div class='metrics-box bordered-box'>
        <div class='metrics-title'>
            Metrics:<br>
        </div>
        Total lines of code: <span id='loc'>{loc}</span><br>
        Total lines skipped (#nosec): <span id='nosec'>{nosec}</span>
    </div>
</span>

"""

    issues = manager.get_issue_list(sev_level=sev_level, conf_level=conf_level)

    baseline = not isinstance(issues, list)

    # build the skipped string to insert in the report
    skipped_str = ''.join('%s - %s\n' % (fname, reason)
                          for fname, reason in manager.skipped)
    if skipped_str:
        skipped_text = skipped_block.format(files_list=skipped_str)
    else:
        skipped_text = ''

    # build the results string to insert in the report
    results_str = ''
    for index, issue in enumerate(issues):
        if not baseline or len(issues[issue]) == 1:
            candidates = ''
            code = code_block.format(code=issue.get_code(lines, True).
                                     strip('\n').lstrip(' '))
        else:
            candidates_str = ''
            code = ''
            for candidate in issues[issue]:
                candidate_code = (candidate.get_code(lines, True).strip('\n').
                                  lstrip(' '))
                candidates_str += candidate_issue.format(code=candidate_code)

            candidates = candidate_block.format(candidate_list=candidates_str)

        results_str += issue_block.format(issue_no=index,
                                          issue_class='issue-sev-{}'.
                                          format(issue.severity.lower()),

                                          test_name=issue.test,
                                          test_text=issue.text,
                                          severity=issue.severity,
                                          confidence=issue.confidence,
                                          path=issue.fname, code=code,
                                          candidates=candidates)

    # build the metrics string to insert in the report
    metrics_summary = metrics_block.format(
        loc=manager.metrics.data['_totals']['loc'],
        nosec=manager.metrics.data['_totals']['nosec'])

    # build the report and output it
    report_contents = report_block.format(metrics=metrics_summary,
                                          skipped=skipped_text,
                                          results=results_str)

    with utils.output_file(filename, 'w') as fout:
        fout.write(header_block)
        fout.write(report_contents)

    if filename is not None:
        logger.info("HTML output written to file: %s" % filename)
