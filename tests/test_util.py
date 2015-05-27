# -*- coding:utf-8 -*-
#
# Copyright 2014 Hewlett-Packard Development Company, L.P.
# Copyright 2015 Nebula, Inc.
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
import os
import shutil
import tempfile
import unittest

from bandit.core import utils as b_utils


def _touch(path):
    '''Create an empty file at ``path``.'''
    newf = open(path, 'w')
    newf.close()


class UtilTests(unittest.TestCase):
    '''This set of tests exercises bandit.core.util functions
    '''

    def setUp(self):
        super(UtilTests, self).setUp()
        self._setup_get_module_qualname_from_path()

    def tearDown(self):
        self._tear_down_get_module_qualname_from_path()

    def _setup_get_module_qualname_from_path(self):
        '''Setup a fake module directory tree for testing
           get_module_qualname_from_path().

           Create temporary directory and then create fake .py files
           within directory structure.  We setup test cases for
           a typical module, a path misssing a middle __init__.py,
           no __init__.py anywhere in path, symlinking .py files.
        '''

        self.tempdir = tempfile.mkdtemp()
        self.reltempdir = os.path.relpath(self.tempdir)

        # good/a/b/c/test_typical.py
        os.makedirs(os.path.join(
            self.tempdir, 'good', 'a', 'b', 'c'), 0o755)
        _touch(os.path.join(self.tempdir, 'good', '__init__.py'))
        _touch(os.path.join(self.tempdir, 'good', 'a', '__init__.py'))
        _touch(os.path.join(
            self.tempdir, 'good', 'a', 'b', '__init__.py'))
        _touch(os.path.join(
            self.tempdir, 'good', 'a', 'b', 'c', '__init__.py'))
        _touch(os.path.join(
            self.tempdir, 'good', 'a', 'b', 'c', 'test_typical.py'))

        # missingmid/a/b/c/test_missingmid.py
        os.makedirs(os.path.join(
            self.tempdir, 'missingmid', 'a', 'b', 'c'), 0o755)
        _touch(os.path.join(self.tempdir, 'missingmid', '__init__.py'))
        # no missingmid/a/__init__.py
        _touch(os.path.join(
            self.tempdir, 'missingmid', 'a', 'b', '__init__.py'))
        _touch(os.path.join(
            self.tempdir, 'missingmid', 'a', 'b', 'c', '__init__.py'))
        _touch(os.path.join(
            self.tempdir, 'missingmid', 'a', 'b', 'c', 'test_missingmid.py'))

        # missingend/a/b/c/test_missingend.py
        os.makedirs(os.path.join(
            self.tempdir, 'missingend', 'a', 'b', 'c'), 0o755)
        _touch(os.path.join(
            self.tempdir, 'missingend', '__init__.py'))
        _touch(os.path.join(
            self.tempdir, 'missingend', 'a', 'b', '__init__.py'))
        # no missingend/a/b/c/__init__.py
        _touch(os.path.join(
            self.tempdir, 'missingend', 'a', 'b', 'c', 'test_missingend.py'))

        # syms/a/bsym/c/test_typical.py
        os.makedirs(os.path.join(self.tempdir, 'syms', 'a'), 0o755)
        _touch(os.path.join(self.tempdir, 'syms', '__init__.py'))
        _touch(os.path.join(self.tempdir, 'syms', 'a', '__init__.py'))
        os.symlink(os.path.join(self.tempdir, 'good', 'a', 'b'),
                   os.path.join(self.tempdir, 'syms', 'a', 'bsym'))

    def _tear_down_get_module_qualname_from_path(self):
        '''Remove temp directory tree from test setup'''
        shutil.rmtree(self.tempdir)

    def test_get_module_qualname_from_path_abs_typical(self):
        '''Test get_module_qualname_from_path with typical absolute paths'''

        name = b_utils.get_module_qualname_from_path(os.path.join(
            self.tempdir, 'good', 'a', 'b', 'c', 'test_typical.py'))
        self.assertEqual('good.a.b.c.test_typical', name)

    def test_get_module_qualname_from_path_abs_missingmid(self):
        '''Test get_module_qualname_from_path with missing module
           __init__.py'''

        name = b_utils.get_module_qualname_from_path(os.path.join(
            self.tempdir, 'missingmid', 'a', 'b', 'c',
            'test_missingmid.py'))
        self.assertEqual('b.c.test_missingmid', name)

    def test_get_module_qualname_from_path_abs_missingend(self):
        '''Test get_module_qualname_from_path with no __init__.py
        in last dir'''

        name = b_utils.get_module_qualname_from_path(os.path.join(
            self.tempdir, 'missingend', 'a', 'b', 'c',
            'test_missingend.py'))
        self.assertEqual('test_missingend', name)

    def test_get_module_qualname_from_path_abs_syms(self):
        '''Test get_module_qualname_from_path with symlink in path'''

        name = b_utils.get_module_qualname_from_path(os.path.join(
            self.tempdir, 'syms', 'a', 'bsym', 'c', 'test_typical.py'))
        self.assertEqual('syms.a.bsym.c.test_typical', name)

    def test_get_module_qualname_from_path_rel_typical(self):
        '''Test get_module_qualname_from_path with typical relative paths'''

        name = b_utils.get_module_qualname_from_path(os.path.join(
            self.reltempdir, 'good', 'a', 'b', 'c', 'test_typical.py'))
        self.assertEqual('good.a.b.c.test_typical', name)

    def test_get_module_qualname_from_path_rel_missingmid(self):
        '''Test get_module_qualname_from_path with module __init__.py
           missing and relative paths'''

        name = b_utils.get_module_qualname_from_path(os.path.join(
            self.reltempdir, 'missingmid', 'a', 'b', 'c',
            'test_missingmid.py'))
        self.assertEqual('b.c.test_missingmid', name)

    def test_get_module_qualname_from_path_rel_missingend(self):
        '''Test get_module_qualname_from_path with __init__.py missing from
           last dir and using relative paths'''

        name = b_utils.get_module_qualname_from_path(os.path.join(
            self.reltempdir, 'missingend', 'a', 'b', 'c',
            'test_missingend.py'))
        self.assertEqual('test_missingend', name)

    def test_get_module_qualname_from_path_rel_syms(self):
        '''Test get_module_qualname_from_path with symbolic relative paths'''

        name = b_utils.get_module_qualname_from_path(os.path.join(
            self.reltempdir, 'syms', 'a', 'bsym', 'c', 'test_typical.py'))
        self.assertEqual('syms.a.bsym.c.test_typical', name)

    def test_get_module_qualname_from_path_sys(self):
        '''Test get_module_qualname_from_path with system module paths'''

        name = b_utils.get_module_qualname_from_path(os.__file__)
        self.assertEqual('os', name)

        # This will fail because of magic for os.path. Not sure how to fix.
        # name = b_utils.get_module_qualname_from_path(os.path.__file__)
        # self.assertEqual(name, 'os.path')

    def test_get_module_qualname_from_path_invalid_path(self):
        '''Test get_module_qualname_from_path with invalid path '''

        name = b_utils.get_module_qualname_from_path('/a/b/c/d/e.py')
        self.assertEqual('e', name)

    def test_get_module_qualname_from_path_dir(self):
        '''Test get_module_qualname_from_path with dir path '''

        with self.assertRaises(b_utils.InvalidModulePath):
            b_utils.get_module_qualname_from_path('/tmp/')

    def test_namespace_path_join(self):
        p = b_utils.namespace_path_join('base1.base2', 'name')
        self.assertEqual('base1.base2.name', p)

    def test_namespace_path_split(self):
        (head, tail) = b_utils.namespace_path_split('base1.base2.name')
        self.assertEqual('base1.base2', head)
        self.assertEqual('name', tail)

    def test_get_call_name1(self):
        '''Gets a qualified call name'''
        tree = ast.parse('a.b.c.d(x,y)').body[0].value
        name = b_utils.get_call_name(tree, {})
        self.assertEqual('a.b.c.d', name)

    def test_get_call_name2(self):
        '''Gets qualified call name and resolves aliases'''
        tree = ast.parse('a.b.c.d(x,y)').body[0].value

        name = b_utils.get_call_name(tree, {'a': 'alias.x.y'})
        self.assertEqual('alias.x.y.b.c.d', name)

        name = b_utils.get_call_name(tree, {'a.b': 'alias.x.y'})
        self.assertEqual('alias.x.y.c.d', name)

        name = b_utils.get_call_name(tree, {'a.b.c.d': 'alias.x.y'})
        self.assertEqual('alias.x.y', name)

    def test_get_call_name3(self):
        '''Getting name for a complex call'''
        tree = ast.parse('a.list[0](x,y)').body[0].value
        name = b_utils._get_attr_qual_name(tree, {})
        self.assertEqual('', name)
        # TODO(ljfisher) At best we might be able to get:
        # self.assertEqual(name, 'a.list[0]')
