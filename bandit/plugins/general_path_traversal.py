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

r"""
===================================================
B112: Test for os.path.join with variables
===================================================

Using os.path.join to combine variable into a single file path can lead to
unintended directory traversal if the variables invovled can be manipulated:

.. code-block: python

    local = read_input() # set to somthing like "../../../"
    path = os.path.join(local, "etc") # system level etc not local

**Config Options:**
None

:Example:

.. code-block: none

    >> Issue: Check variables used with os.path.join are trusted or sanitised.
       Severity: Low   Confidence: Low
       Location: ./examples/os_path_join.py:2
    1 f = os.path.join(local, "etc")
    2 f.write('blah')

.. seealso::

.. versionadded:: 0.17.2

"""

import ast

import bandit
from bandit.core import test_properties as test


@test.checks('Call')
@test.test_id('B112')
def os_path_join_traversal(context):
    if context.call_function_name_qual == 'os.path.join':
        for arg in context.node.args:
            if isinstance(arg, ast.Name):
                return bandit.Issue(
                    severity=bandit.LOW,
                    confidence=bandit.LOW,
                    text="Check variables used with os.path.join are trusted"
                         " or sanitised.")
