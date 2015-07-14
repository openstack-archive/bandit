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
from bandit.core.test_properties import *
from bandit.core import utils


@checks('Call')
def paramiko_calls(context):
    for module in ['paramiko']:
        if context.is_module_imported_like(module):
            if context.call_function_name in ['exec_command', 'invoke_shell']:
                return bandit.Issue(severity=bandit.MEDIUM, 
                                    confidence=bandit.MEDIUM,
                                    text='Probable paramiko shell execution, check inputs')
