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


def _get(node, bits, stop):
    if node != stop:
        bits.append(
            _get(node.left, bits, stop) if isinstance(node.left, ast.BinOp)
            else node.left)
        bits.append(
            _get(node.right, bits, stop) if isinstance(node.right, ast.BinOp)
            else node.right)


def _evaluate_ast(node):
    stop = node.parent
    bits = [node]
    names = ['execute', 'executemany']
    while isinstance(node.parent, ast.BinOp):
        node = node.parent
    if isinstance(node, ast.BinOp):
        _get(node, bits, stop)
        out = " ".join([x.s for x in bits if isinstance(x, ast.Str)])

        if isinstance(node.parent, ast.Call):  # wrapped in "exectue" call?
            name = (node.parent.func.attr if
                    isinstance(node.parent.func, ast.Attribute)
                    else node.parent.func.id)
            return (name in names, out)
        return (False, out)
    return (False, "")


@checks('Str')
def hardcoded_sql_expressions(context):
    val = _evaluate_ast(context.node)
    if _check_string(val[1]):
        return bandit.Issue(
            severity=bandit.MEDIUM,
            confidence=bandit.MEDIUM if val[0] else bandit.LOW,
            text="Possible SQL injection vector through string-based "
                 "query construction."
        )
