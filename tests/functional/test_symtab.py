# -*- coding:utf-8 -*-
#
# Copyright 2015 Hewlett-Packard Development Company, L.P.
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

import os
import ast

import six
import testtools
import textwrap
import mock

from bandit.core import constants
from bandit.core import node_visitor


class SymtabTests(testtools.TestCase):

    def setUp(self):
        super(SymtabTests, self).setUp()
        self.visitor = node_visitor.BanditNodeVisitor(
            "none", None, None, None, False, False)

    def tearDown(self):
        super(SymtabTests, self).tearDown()

    def run_example(self, example):
        '''A helper method to run the specified test

        This method runs the node visitor over a block of python given as a
        string. We dont bother with a manager or any actual test plugins, the
        symtab tests just need the node visitor to process the AST and populate
        the table.
        '''
        with mock.patch('bandit.core.tester.BanditTester.run_tests') as m:
            m.return_value=scores = {
                'SEVERITY': [0] * len(constants.RANKING),
                'CONFIDENCE': [0] * len(constants.RANKING)
            }
            self.visitor.process(sdata=example)

    def test_populate(self):
        exp = textwrap.dedent("""
        class a:
            class c:
                def e():
                    pass

            def a():
                pass

            def b():
                pass

        def f():
            pass
        """)
        self.run_example(exp)
        self.assertEqual(self.visitor.symtab.get_definition('f').name, 'f')
        self.assertEqual(self.visitor.symtab.get_definition('a.c.e').name, 'e')
        self.assertEqual(self.visitor.symtab.get_definition('a.a').name, 'a')
        self.assertEqual(self.visitor.symtab.get_definition('a.b').name, 'b')

    def test_scopes(self):
        name = 'bandit.core.node_visitor.BanditNodeVisitor.visit_Str'
        with mock.patch(name) as m:
            def func(vis, node):
                self.assertEqual(len(vis.symtab.scopes), 2)
                vis.generic_visit(node)

            m.visit_Str = func
            exp = textwrap.dedent("""
            def a():
                def b():
                    pass
                a = "str"
            """)
            self.run_example(exp)
            self.assertEqual(len(self.visitor.symtab.scopes), 1)

    def test_symbols(self):
        exp = textwrap.dedent("""
        b = 1
        a = "str"
        """)

        self.run_example(exp)
        sym = self.visitor.symtab.get_symbol('b')
        self.assertTrue(isinstance(sym, ast.Num))
        self.assertEqual(1, sym.n)

        sym = self.visitor.symtab.get_symbol('a')
        self.assertTrue(isinstance(sym, ast.Str))
        self.assertEqual('str', sym.s)

    def test_var_expansion(self):
        exp = textwrap.dedent("""
        a = "str "
        c = "and" + " some " + "more "
        b = a + c + a * (4 / 2)
        """)

        self.run_example(exp)
        sym = self.visitor.symtab.get_symbol('b')
        val = self.visitor.symtab.resolve_binop_chain(sym)
        self.assertEqual('str and some more str str ', val.s)

    def test_arg_expansion(self):
        exp = textwrap.dedent("""
        def foo(a, b):
            c = a + b

        foo("one ", "two")
        """)

        name = 'bandit.core.symtab.SymbolTable.pop_scope'
        with mock.patch(name) as m: # mock out pop so we keep the last scope
            self.run_example(exp)

        sym = self.visitor.symtab.get_symbol('c')
        val = self.visitor.symtab.resolve_binop_chain(sym)
        self.assertEqual('one two', val.s)
