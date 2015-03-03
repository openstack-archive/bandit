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

import os

import unittest
import inspect

from bandit.core import constants as C
from bandit.core import manager as b_manager
from bandit.core import test_set as b_test_set


cfg_file = os.path.join(os.getcwd(), 'bandit.yaml')


class FunctionalTests(unittest.TestCase):

    '''This set of tests runs bandit against each example file in turn
    and records the score returned. This is compared to a known good value.
    When new tests are added to an example the expected result should be
    adjusted to match.
    '''

    def setUp(self):
        super(FunctionalTests, self).setUp()
        # NOTE(tkelsey): bandit is very sensitive to paths, so stitch
        # them up here for the testing environment.
        #
        path = os.path.join(os.getcwd(), 'bandit', 'plugins')
        self.b_mgr = b_manager.BanditManager(cfg_file, 'file')
        self.b_mgr.b_conf._settings['plugins_dir'] = path
        self.b_mgr.b_ts = b_test_set.BanditTestSet(self.b_mgr.logger,
                                                   config=self.b_mgr.b_conf,
                                                   profile=None)

    def tearDown(self):
        pass

    def check_example(self, example_script, info=0, warn=0, error=0):
        '''A helper method to test the scores for example scripts.

        :param example_script: Path to the script to test
        :param info: The expected number of INFO-level issues to find
        :param warn: The expected number of WARN-level issues to find
        :param error: The expected number of ERROR-level issues to find
        '''
        path = os.path.join(os.getcwd(), 'examples', example_script)
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        expected = (info * C.SEVERITY_VALUES['INFO'] +
                    warn * C.SEVERITY_VALUES['WARN'] +
                    error * C.SEVERITY_VALUES['ERROR'])
        self.assertEqual(expected, self.b_mgr.scores[0])

    def test_binding(self):
        '''Test the bind-to-0.0.0.0 example.'''
        self.check_example('binding.py', warn=1)

    def test_call_tests(self):
        '''Test the `subprocess.call` example.'''
        self.check_example('call-tests.py', info=1, warn=1)

    def test_crypto_md5(self):
        path = os.path.join(os.getcwd(), 'examples', 'crypto-md5.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(25, self.b_mgr.scores[0])

    def test_eval(self):
        path = os.path.join(os.getcwd(), 'examples', 'eval.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(15, self.b_mgr.scores[0])

    def test_exec(self):
        path = os.path.join(os.getcwd(), 'examples', 'exec.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(20, self.b_mgr.scores[0])

    def test_exec_as_root(self):
        path = os.path.join(os.getcwd(), 'examples', 'exec-as-root.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        expected = 5 * C.SEVERITY_VALUES['INFO']
        self.assertEqual(expected, self.b_mgr.scores[0])

    def test_hardcoded_passwords(self):
        path = os.path.join(os.getcwd(), 'examples', 'hardcoded-passwords.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(0, self.b_mgr.scores[0])  # seems broken.

    def test_hardcoded_tmp(self):
        path = os.path.join(os.getcwd(), 'examples', 'hardcoded-tmp.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(5, self.b_mgr.scores[0])

    def test_httplib_https(self):
        path = os.path.join(os.getcwd(), 'examples', 'httplib_https.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(5, self.b_mgr.scores[0])

    def test_imports_aliases(self):
        path = os.path.join(os.getcwd(), 'examples', 'imports-aliases.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(43, self.b_mgr.scores[0])

    def test_imports_from(self):
        path = os.path.join(os.getcwd(), 'examples', 'imports-from.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(3, self.b_mgr.scores[0])

    def test_imports_function(self):
        path = os.path.join(os.getcwd(), 'examples', 'imports-function.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(2, self.b_mgr.scores[0])

    def test_imports_telnetlib(self):
        path = os.path.join(os.getcwd(), 'examples', 'imports-telnetlib.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(10, self.b_mgr.scores[0])

    def test_imports(self):
        path = os.path.join(os.getcwd(), 'examples', 'imports.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(2, self.b_mgr.scores[0])

    def test_mktemp(self):
        path = os.path.join(os.getcwd(), 'examples', 'mktemp.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(20, self.b_mgr.scores[0])

    def test_nonesense(self):
        path = os.path.join(os.getcwd(), 'examples', 'nonesense.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(0, len(self.b_mgr.scores))

    def test_okay(self):
        path = os.path.join(os.getcwd(), 'examples', 'okay.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(0, self.b_mgr.scores[0])

    def test_os_exec(self):
        path = os.path.join(os.getcwd(), 'examples', 'os-exec.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(0, self.b_mgr.scores[0])  # seems broken.

    def test_os_popen(self):
        path = os.path.join(os.getcwd(), 'examples', 'os-popen.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(20, self.b_mgr.scores[0])

    def test_os_spawn(self):
        path = os.path.join(os.getcwd(), 'examples', 'os-spawn.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(0, self.b_mgr.scores[0])  # seems broken.

    def test_os_startfile(self):
        path = os.path.join(os.getcwd(), 'examples', 'os-startfile.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(15, self.b_mgr.scores[0])

    def test_pickle(self):
        path = os.path.join(os.getcwd(), 'examples', 'pickle.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(11, self.b_mgr.scores[0])

    def test_random(self):
        path = os.path.join(os.getcwd(), 'examples', 'random.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(3, self.b_mgr.scores[0])

    def test_requests_ssl_verify_disabled_aliases(self):
        path = os.path.join(os.getcwd(), 'examples',
            'requests-ssl-verify-disabled-aliases.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(20, self.b_mgr.scores[0])

    def test_requests_ssl_verify_disabled(self):
        path = os.path.join(os.getcwd(), 'examples',
            'requests-ssl-verify-disabled.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(20, self.b_mgr.scores[0])

    def test_skip(self):
        path = os.path.join(os.getcwd(), 'examples', 'skip.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(35, self.b_mgr.scores[0])

    def test_sql_statements_with_sqlalchemy(self):
        path = os.path.join(os.getcwd(), 'examples',
            'sql_statements_with_sqlalchemy.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(4, self.b_mgr.scores[0])

    def test_sql_statements_without_sql_alchemy(self):
        path = os.path.join(os.getcwd(), 'examples',
            'sql_statements_without_sql_alchemy.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(20, self.b_mgr.scores[0])

    def test_ssl_insecure_version(self):
        path = os.path.join(os.getcwd(), 'examples', 'ssl-insecure-version.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(121, self.b_mgr.scores[0])

    def test_subprocess_call_linebreaks(self):
        path = os.path.join(os.getcwd(), 'examples',
            'subprocess-call-linebreaks.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(6, self.b_mgr.scores[0])

    def test_subprocess_call(self):
        path = os.path.join(os.getcwd(), 'examples', 'subprocess-call.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(6, self.b_mgr.scores[0])

    def test_subprocess_popen_shell(self):
        path = os.path.join(os.getcwd(), 'examples',
            'subprocess-popen-shell.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(21, self.b_mgr.scores[0])

    def test_subprocess_popen_shell2(self):
        path = os.path.join(os.getcwd(), 'examples',
            'subprocess-popen-shell2.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(16, self.b_mgr.scores[0])

    def test_urlopen(self):
        path = os.path.join(os.getcwd(), 'examples', 'urlopen.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(30, self.b_mgr.scores[0])

    def test_utils_shell(self):
        path = os.path.join(os.getcwd(), 'examples', 'utils-shell.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(60, self.b_mgr.scores[0])

    def test_wildcard_injection(self):
        path = os.path.join(os.getcwd(), 'examples', 'wildcard-injection.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(81, self.b_mgr.scores[0])

    def test_yaml(self):
        path = os.path.join(os.getcwd(), 'examples', 'yaml_load.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(5, self.b_mgr.scores[0])

    def test_jinja2_templating(self):
        path = os.path.join(os.getcwd(), 'examples', 'jinja2_templating.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        self.assertEqual(4, self.b_mgr.results_count)
        self.assertEqual(35, self.b_mgr.scores[0])

    def test_secret_config_option(self):
        path = os.path.join(os.getcwd(), 'examples', 'secret-config-option.py')
        self.b_mgr.discover_files([path], True)
        self.b_mgr.run_tests()
        expected = 2 * C.SEVERITY_VALUES['WARN'] + C.SEVERITY_VALUES['INFO']
        self.assertEqual(expected, self.b_mgr.scores[0])
