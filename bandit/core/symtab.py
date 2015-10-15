
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

import ast
import numbers
import pprint

import six


class Scope(object):
    def __init__(self, node=None):
        self.node = node
        self.globals = []
        self.body = {}


class SymbolTable(object):
    def __init__(self):
        self.definitions = {}
        self.scopes = [Scope()]

    def note_assignment(self, node):
        scope = self.scopes[0]
        for targ in node.targets:
            if isinstance(targ, ast.Name):
                if targ.id in scope.globals:
                    # globals are a PITA, but lets do our best
                    self.scopes[-1].body[targ.id] = node.value
                else:
                    scope.body[targ.id] = node.value

    def push_scope(self, node, qualname):
        scope = Scope(node)
        # TODO(tkelsey): handle globals ....

        # using our stored definition, populate arguments that we know about
        try:
            fdef = self.get_definition(qualname)
            for idx, arg in enumerate(node.args):
                scope.body[fdef.args.args[idx].id] = arg
            for kwd in node.keywords:
                scope.body[kwd.arg] = kwd.value
        except Exception:
            pass  # nosec(tkelsey): we have no def for the func, ext module

        self.scopes.insert(0, scope)

    def pop_scope(self):
        self.scopes = self.scopes[1:]
        pass

    def dump(self):
        print("=== definitions ===")
        pprint.pprint(self.definitions)
        for scope in self.scopes:
            print("===== scope =====")
            print("globals:", scope.globals)
            for key, val in six.iteritems(scope.body):
                print("%s: %s" % (key, ast.dump(val)))
        print("===== done =====\n\n")

    def get_symbol(self, name):
        return (self.scopes[-1].body[name]
                if name in self.scopes[-1].body
                else self.scopes[0].body[name])

    def get_definition(self, qualname):
        defs = self.definitions
        for bit in qualname.split('.'):
            defs = defs[bit]
        return defs

    def populate(self, module):
        def _note_classdef(clazz, defs):
            for node in clazz.body:
                if isinstance(node, ast.ClassDef):
                    defs[node.name] = {}
                    _note_classdef(node, defs[node.name])
                elif isinstance(node, ast.FunctionDef):
                    # TODO(tkelsey): handle globals ....
                    defs[node.name] = node

        for node in module.body:
            if isinstance(node, ast.ClassDef):
                self.definitions[node.name] = {}
                _note_classdef(node, self.definitions[node.name])
            elif isinstance(node, ast.FunctionDef):
                # TODO(tkelsey): handle globals ....
                self.definitions[node.name] = node

    # now do clever things with all that data #######

    def _do_binop(self, node):
        lut = {
            'Num': lambda a: a.n,
            'Str': lambda a: a.s,
            'Add': lambda a, b: a + b,
            'Sub': lambda a, b: a - b,
            'Mult': lambda a, b: a * b,
            'Div': lambda a, b: a / b
        }

        try:
            res = (lut[node.op.__class__.__name__](
                   lut[node.left.__class__.__name__](node.left),
                   lut[node.right.__class__.__name__](node.right)))

            if isinstance(res, basestring):
                return ast.Str(res)
            if isinstance(res, numbers.Number):
                return ast.Num(res)

        except Exception:
            return ast.Str("UNRESOLVED")

    def resolve_binop_chain(self, node):
        l = (self.resolve_binop_chain(node.left)
             if isinstance(node.left, ast.BinOp)
             else node.left)

        r = (self.resolve_binop_chain(node.right)
             if isinstance(node.right, ast.BinOp)
             else node.right)

        if isinstance(l, ast.Name):
            l = self.get_symbol(l.id)
            if isinstance(l, ast.BinOp):
                l = self.resolve_binop_chain(l)

        if isinstance(r, ast.Name):
            r = self.get_symbol(r.id)
            if isinstance(r, ast.BinOp):
                r = self.resolve_binop_chain(r)

        n = ast.BinOp(l, node.op, r, lineno=0, col_offset=0)
        return self._do_binop(n)


def _get_binop_root(node):
    if node.parent:
        while isinstance(node.parent, ast.BinOp):
            node = node.parent
    return node
