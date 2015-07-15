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


def _check_string(data):
    val = data.lower()
    return ((val.startswith('select ') and ' from ' in val) or
            val.startswith('insert into') or
            (val.startswith('update ') and ' set ' in val) or
            val.startswith('delete from '))


@checks('Call')
def hardcoded_sql_execute(context):
    if context.call_function_name in ['execute', 'executemany']:
        node = context.node
        if len(node.args) and isinstance(node.args[0], ast.BinOp):
            val = node.args[0].left
            if isinstance(val, ast.Str) and _check_string(val.s):
                return bandit.Issue(
                    severity=bandit.MEDIUM,
                    confidence=bandit.MEDIUM,
                    text="Possible SQL injection vector through string-based "
                         "query construction."
                )


@checks('Str')
def hardcoded_sql_expressions(context):
    enclosing = context.node.parent
    if(isinstance(enclosing, ast.BinOp) and
       not isinstance(enclosing.parent, ast.Call)):
        if _check_string(context.node.s):
            return bandit.Issue(
                severity=bandit.MEDIUM,
                confidence=bandit.LOW,
                text="Possible SQL injection vector through string-based "
                     "query construction."
            )
