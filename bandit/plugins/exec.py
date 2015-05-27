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
import sys

import bandit
from bandit.core import constants
from bandit.core.test_properties import *


def exec_issue():
    return bandit.Issue(
        severity=constants.MEDIUM,
        confidence=constants.HIGH,
        text="Use of exec detected."
    )


if sys.version_info < (3, 0):
    @checks('Exec')
    def exec_used(context):
        return exec_issue()
else:
    @checks('Call')
    def exec_called(context):
        if context.call_function_qual_name == 'exec':
            return exec_issue()
