# Copyright (c) 2018 VMware, Inc.
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
==========================================
B507: Test for missing host key validation
==========================================

Encryption in general is typically critical to the security of many
applications.  Using SSH can greatly increase security by guaranteeing the
identity of the party you are communicating with.  This is accomplished by one
or both parties presenting trusted host keys during the connection
initialization phase of SSH.

When paramiko methods are used, host keys are verified by default. If host key
verification is disabled, Bandit will return a HIGH severity error.

:Example:


.. versionadded:: 1.4.2

"""

import bandit
from bandit.core import test_properties as test


@test.checks('Call')
@test.test_id('B507')
def ssh_no_host_key_verification(context):

    if (context.call_function_name_qual in ['paramiko.client'] and
            context.call_function_name in ['set_missing_host_key_policy']):
        if (['AutoAddPolicy', 'WarningPolicy'] in
                context.get_call_arg_at_position(0)):
            issue = bandit.Issue(
                severity=bandit.HIGH,
                confidence=bandit.HIGH,
                text='Paramiko call with policy set to automatically trust '
                     'the unknown host key.',
                lineno=context.get_lineno_for_call_arg(
                    'set_missing_host_key_policy'),
            )
            return issue
