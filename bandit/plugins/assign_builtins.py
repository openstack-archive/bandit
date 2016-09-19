# -*- coding:utf-8 -*-
#
# Copyright 2016 Hewlett-Packard Development Company, L.P.
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

import ast

import bandit
from bandit.core import test_properties as test

@test.checks('Assign')
@test.test_id('B113')
def assign_builtin(context):
    """**B113: Test for assignment of builtins**

    Assigning to a builtin mechanism in Python has very few legitimate uses,
    but can be a mechanism to confuse protection logic for malicious intent.
    This plugin looks for an assignment to any key within the __builtins__
    dict.

    **Config Options:**

    None

    :Example:

    .. code-block:: none

        >> Issue: [B113:assign_builtin] Assign to __builtins__
           Severity: Medium   Confidence: High
           Location: ./examples/assign-true-false.py:1
        1	__builtins__.False, __builtins__.True = True, False

    .. seealso::

        - https://access.redhat.com/blogs/766093/posts/2592591

    .. versionadded:: 1.2

    """
    for target in context.node.targets:
        if isinstance(target, ast.Tuple):
            for elt in target.elts:
                if elt.value.id == '__builtins__':
                    return bandit.Issue(
                        severity=bandit.MEDIUM,
                        confidence=bandit.HIGH,
                        text="Assign to __builtins__"
                    )
