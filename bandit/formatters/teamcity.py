import logging
import sys

from bandit.core import test_properties
from bandit.formatters import utils
from bandit.formatters.code_mapping import CODE_MAPPING

LOG = logging.getLogger(__name__)

SEVERITY_MAPPING = {'UNDEFINED': 'WARNING',
                    'LOW': 'WARNING',
                    'MEDIUM': 'ERROR',
                    'HIGH': 'ERROR'}

issue_types_output = set()


def _output_issue_type(issue):
    if issue.test_id not in issue_types_output:
        issue_types_output.add(issue.test_id)

        return ["##teamcity[inspectionType "
                "id='bandit_{test_id}' "
                "name='{test_name}' "
                "category='Bandit' "
                "description='{test_description}']".format(test_id=issue.test_id,
                                                           test_description=issue.test,
                                                           test_name='{test_id}: {description}'
                                                                     .format(test_id=issue.test_id,
                                                                             description=CODE_MAPPING[issue.test_id]
                                                                                          .replace('|', '||')
                                                                                          .replace('\'', '|\'')))]

    return []


def _output_issue_str(issue):
    # returns a list of lines that should be added to the existing lines list
    bits = []

    # make sure the issue type is present
    bits.extend(_output_issue_type(issue))

    bits.append("##teamcity[inspection "
                "typeId='bandit_{test_id}' "
                "message='{message}' "
                "file='{filename}' "
                "line='{lineno}' "
                "SEVERITY='{severity}' "
                "CONFIDENCE='{confidence}']".format(test_id=issue.test_id,
                                                    message=issue.text.replace('|', '||').replace('\'', '|\''),
                                                    filename=issue.fname,
                                                    lineno=issue.lineno,
                                                    severity=SEVERITY_MAPPING[issue.severity],
                                                    confidence=issue.confidence))

    return '\n'.join([bit for bit in bits])


def get_results(manager, sev_level, conf_level, lines):
    bits = []
    issues = manager.get_issue_list(sev_level, conf_level)
    baseline = not isinstance(issues, list)

    if not len(issues):
        return ""

    for issue in issues:
        if not baseline or len(issues[issue]) == 1:
            bits.append(_output_issue_str(issue))
        else:
            for candidate in issues[issue]:
                bits.append(_output_issue_str(candidate))

    return '\n'.join([bit for bit in bits])


@test_properties.accepts_baseline
def report(manager, fileobj, sev_level, conf_level, lines=-1):
    result = get_results(manager, sev_level, conf_level, lines)

    with fileobj:
        wrapped_file = utils.wrap_file_object(fileobj)
        wrapped_file.write(utils.convert_file_contents(result))

    if fileobj.name != sys.stdout.name:
        LOG.info("TeamCity output written to file: %s", fileobj.name)
