#    Copyright 2016 IBM Corp.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import os

import fixtures
from mock import patch
import testtools

from bandit.cli import main as bandit
from bandit.core import utils

bandit_config_content = """
[bandit]
"""


class BanditCLIMainLoggerTests(testtools.TestCase):

    def setUp(self):
        super(BanditCLIMainLoggerTests, self).setUp()
        self.logger = logging.getLogger()
        self.original_logger_handlers = self.logger.handlers
        self.original_logger_level = self.logger.level
        self.logger.handlers = []

    def tearDown(self):
        super(BanditCLIMainLoggerTests, self).tearDown()
        self.logger.handlers = self.original_logger_handlers
        self.logger.level = self.original_logger_level

    def test_init_logger(self):
        # Test that a logger was properly initialized
        bandit._init_logger(False)

        self.assertIsNotNone(self.logger)
        self.assertNotEqual(self.logger.handlers, [])
        self.assertEqual(self.logger.level, logging.INFO)

    def test_init_logger_debug_mode(self):
        # Test that the logger's level was set at 'DEBUG'
        bandit._init_logger(True)
        self.assertEqual(self.logger.level, logging.DEBUG)


class BanditCLIMainTests(testtools.TestCase):

    def test_get_options_from_ini_no_ini_path_no_target(self):
        # Test that no config options are loaded when no ini path or target
        # directory are provided
        self.assertIsNone(bandit._get_options_from_ini(None, []))

    def test_get_options_from_ini_empty_directory_no_target(self):
        # Test that no config options are loaded when an empty directory is
        # provided as the ini path and no target directory is provided
        ini_directory = self.useFixture(fixtures.TempDir()).path
        self.assertIsNone(bandit._get_options_from_ini(ini_directory, []))

    def test_get_options_from_ini_no_ini_path_no_bandit_files(self):
        # Test that no config options are loaded when no ini path is provided
        # and the target directory contains no bandit config files (.bandit)
        target_directory = self.useFixture(fixtures.TempDir()).path
        self.assertIsNone(bandit._get_options_from_ini(None,
                          [target_directory]))

    def test_get_options_from_ini_no_ini_path_multi_bandit_files(self):
        # Test that bandit exits when no ini path is provided and the target
        # directory(s) contain multiple bandit config files (.bandit)
        target_directory = self.useFixture(fixtures.TempDir()).path
        second_config = 'second_config_directory'
        os.mkdir(os.path.join(target_directory, second_config))
        bandit_config_one = os.path.join(target_directory, '.bandit')
        bandit_config_two = os.path.join(target_directory, second_config,
                                         '.bandit')
        bandit_files = [bandit_config_one, bandit_config_two]
        for bandit_file in bandit_files:
            with open(bandit_file, 'wt') as fd:
                fd.write(bandit_config_content)
        self.assertRaisesRegex(SystemExit, '2', bandit._get_options_from_ini,
                               None, [target_directory])

    def test_init_extensions(self):
        # Test that an extension loader manager is returned
        from bandit.core import extension_loader as ext_loader
        self.assertEqual(bandit._init_extensions(), ext_loader.MANAGER)

    def test_log_option_source_arg_val(self):
        # Test that the command argument value is returned when provided
        arg_val = 'file'
        ini_val = 'vuln'
        option_name = 'aggregate'
        self.assertEqual(bandit._log_option_source(arg_val, ini_val,
                         option_name), arg_val)

    def test_log_option_source_ini_value(self):
        # Test that the ini value is returned when no command argument is
        # provided
        ini_val = 'vuln'
        option_name = 'aggregate'
        self.assertEqual(bandit._log_option_source(None, ini_val,
                         option_name), ini_val)

    def test_log_option_source_no_values(self):
        # Test that None is returned when no command arguement or ini value are
        # provided
        option_name = 'aggregate'
        self.assertIsNone(bandit._log_option_source(None, None, option_name))

    @patch('sys.argv', ['bandit', 'test'])
    def test_main_no_config(self):
        # Test that bandit exits when a config file cannot be found, raising a
        # NoConfigFileFound error
        with patch('bandit.cli.main._find_config') as mock_find_config:
            mock_find_config.side_effect = utils.NoConfigFileFound('')
            # assert a SystemExit with code 2
            self.assertRaisesRegex(SystemExit, '2', bandit.main)


class BanditCLIMainFindConfigTests(testtools.TestCase):

    def setUp(self):
        super(BanditCLIMainFindConfigTests, self).setUp()
        self.current_directory = os.getcwd()

    def tearDown(self):
        super(BanditCLIMainFindConfigTests, self).tearDown()
        os.chdir(self.current_directory)

    def test_find_config_no_config(self):
        # Test that a utils.NoConfigFileFound error is raised when no config
        # file is found
        with patch('os.path.isfile') as mock_os_path_isfile:
            # patch to make sure no config files can be found
            mock_os_path_isfile.return_value = False
            self.assertRaises(utils.NoConfigFileFound, bandit._find_config)

    def test_find_config_local_config(self):
        # Test that when a config file is found is current directory, it is
        # used as the config file
        temp_directory = self.useFixture(fixtures.TempDir()).path
        os.chdir(temp_directory)
        local_config = "./bandit.yaml"
        with open(local_config, 'wt') as fd:
            fd.write(bandit_config_content)
        self.assertEqual(bandit._find_config(), local_config)
