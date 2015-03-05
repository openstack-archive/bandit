# -*- coding:utf-8 -*-
#
# Copyright 2014 Hewlett-Packard Development Company, L.P.
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

import bandit
from bandit.core.test_properties import checks


# Callables in the subprocess module: watch for `shell=True`.
SUBPROCESS_MODULE_FUNCTIONS = set(['subprocess.Popen',
                                   'subprocess.call',
                                   'subprocess.check_call',
                                   'subprocess.check_output'])

# Callables that are vulnerable to shell injection.
SHELL_INJECTION_FUNCTIONS = set(['os.system', 'os.popen', 'os.popen2',
                                 'os.popen3', 'os.popen4', 'popen2.popen2',
                                 'popen2.popen3', 'popen2.popen4',
                                 'popen2.Popen3', 'popen2.Popen4',
                                 'commands.getoutput',
                                 'commands.getstatusoutput'])

# Callables that run processes but don't interpret shell metacharacters.
PROCESS_FUNCTIONS_NO_SUBSHELL = set(['os.execl', 'os.execle', 'os.execlp',
                                     'os.execlpe', 'os.execv', 'os.execve',
                                     'os.execvp', 'os.execvpe', 'os.spawnl',
                                     'os.spawnle', 'os.spawnlp', 'os.spawnlpe',
                                     'os.spawnv', 'os.spawnve', 'os.spawnvp',
                                     'os.spawnvpe', 'os.startfile'])

# All standard library functions that can launch a process.
ALL_PROCESS_FUNCTIONS = (SUBPROCESS_MODULE_FUNCTIONS |
                         SHELL_INJECTION_FUNCTIONS |
                         PROCESS_FUNCTIONS_NO_SUBSHELL)

# Callables from the subprocess module, plus wrappers from OpenStack.
SUBPROCESS_AND_HELPERS = (set(['utils.execute',
                               'utils.execute_with_timeout'])
                          | SUBPROCESS_MODULE_FUNCTIONS)


@checks('Call')
def subshell_functions(context):
    function_name_qual = context.call_function_name_qual
    if function_name_qual in SHELL_INJECTION_FUNCTIONS:
        return (bandit.ERROR, 'Dangerous function "%s": check for shell '
                'injection.' % function_name_qual)
    elif function_name_qual in PROCESS_FUNCTIONS_NO_SUBSHELL:
        return (bandit.WARN, 'Caution: starting an external process.')


@checks('Call')
def subprocess_popen_with_shell_equals_true(context):
    if context.call_function_name_qual in SUBPROCESS_AND_HELPERS:

        if context.check_call_arg_value('shell', 'True'):
            return (bandit.ERROR, 'subprocess call with shell=True '
                    'identified, security issue.  %s' %
                    context.call_args_string)
        else:
            return (bandit.WARN, 'subprocess call without shell=True, '
                    'potential security issue.')


@checks('Call')
def any_other_function_with_shell_equals_true(context):
    # Alerts on any function call that includes a shell=True parameter
    # (multiple 'helpers' with varying names have been identified across
    # various OpenStack projects).
    if context.call_function_name_qual not in SUBPROCESS_AND_HELPERS:
        if context.check_call_arg_value('shell', 'True'):

            return(bandit.WARN, 'Function call with shell=True '
                   'parameter identified, possible security issue.  %s' %
                   context.call_args_string)
