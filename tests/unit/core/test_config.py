# Copyright 2015 IBM Corp.
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


import logging
import os
import tempfile
import unittest

import fixtures
import mock
import testtools

from bandit.core import config


LOG = logging.getLogger('bandit.test')
SAMPLE_CONFIG_FILE = os.path.join(os.getcwd(), 'bandit/config/bandit.yaml')

class TestInit(testtools.TestCase):
    def test_settings(self):
        # Can initialize a BanditConfig.

        b_config = config.BanditConfig(LOG, SAMPLE_CONFIG_FILE)

        # After initialization, can get settings.
        self.assertEqual(50, b_config.get_setting('progress'))
        self.assertEqual('', b_config.get_setting('color_HEADER'))
        self.assertEqual('', b_config.get_setting('color_DEFAULT'))
        self.assertEqual('', b_config.get_setting('color_LOW'))
        self.assertEqual('', b_config.get_setting('color_MEDIUM'))
        self.assertEqual('', b_config.get_setting('color_HIGH'))
        self.assertEqual('*.py', b_config.get_setting('plugin_name_pattern'))

        # config property is the parsed bandit.yaml, using plugin_name_pattern
        # for the test (anything in bandit.yaml could be used instead).
        self.assertEqual('*.py', b_config.config['plugin_name_pattern'])

        # After initialization, can get options from config.
        self.assertEqual('*.py', b_config.get_option('plugin_name_pattern'))

    def test_file_does_not_exist(self):
        # When the config file doesn't exist, sys.exit(2) is called.

        cfg_file = os.path.join(os.getcwd(), 'notafile')

        m = self.useFixture(
            fixtures.MockPatch('sys.exit', side_effect=Exception)).mock

        self.assertRaises(Exception, config.BanditConfig, LOG, cfg_file)

        m.assert_called_once_with(2)

    def test_yaml_invalid(self):
        # When the config yaml file isn't valid, sys.exit(2) is called.

        with tempfile.NamedTemporaryFile(delete=False) as f:
            # The following is invalid because it starts a sequence and doesn't
            # end it.
            invalid_yaml = '- [ something'
            f.write(invalid_yaml)

        self.addCleanup(os.unlink, f.name)

        cfg_file = os.path.join(os.getcwd(), f.name)

        m = self.useFixture(
            fixtures.MockPatch('sys.exit', side_effect=Exception)).mock

        self.assertRaises(Exception, config.BanditConfig, LOG, cfg_file)

        m.assert_called_once_with(2)

    def test_progress_conf_setting(self):
        # The progress setting can be set in bandit.yaml via
        # show_progress_any.

        with tempfile.NamedTemporaryFile(delete=False) as f:
            # The following is invalid because it starts a sequence and doesn't
            # end it.
            sample_yaml = 'show_progress_every: 23'
            f.write(sample_yaml)

        self.addCleanup(os.unlink, f.name)

        b_config = config.BanditConfig(LOG, f.name)
        self.assertEqual(23, b_config.get_setting('progress'))

    def test_colors_isatty_defaults(self):
        # When stdout says it's a tty there are default colors.

        self.useFixture(
            fixtures.MockPatch('sys.stdout.isatty', return_value=True))

        b_config = config.BanditConfig(LOG, SAMPLE_CONFIG_FILE)

        self.assertEqual('\x1b[95m', b_config.get_setting('color_HEADER'))
        self.assertEqual('\x1b[0m', b_config.get_setting('color_DEFAULT'))
        self.assertEqual('\x1b[94m', b_config.get_setting('color_LOW'))
        self.assertEqual('\x1b[93m', b_config.get_setting('color_MEDIUM'))
        self.assertEqual('\x1b[91m', b_config.get_setting('color_HIGH'))

    def test_colors_isatty_config(self):
        # When stdout says it's a tty the colors can be set in bandit.yaml

        self.useFixture(
            fixtures.MockPatch('sys.stdout.isatty', return_value=True))

        with tempfile.NamedTemporaryFile(delete=False) as f:
            # The following is invalid because it starts a sequence and doesn't
            # end it.
            sample_yaml = """
output_colors:
  HEADER: '\\033[23m'
"""
            f.write(sample_yaml)

        self.addCleanup(os.unlink, f.name)

        b_config = config.BanditConfig(LOG, f.name)

        self.assertEqual('\x1b[23m', b_config.get_setting('color_HEADER'))


class TestGetOption(testtools.TestCase):
    def setUp(self):
        super(TestGetOption, self).setUp()
        self.b_config = config.BanditConfig(LOG, SAMPLE_CONFIG_FILE)

    def test_levels(self):
        # get_option with .-separated string.

        # For the test, just pick an option from the config file.
        sample_option_name = 'hardcoded_password.word_list'
        self.assertEqual('%(site_data_dir)s/wordlist/default-passwords',
                         self.b_config.get_option(sample_option_name))

    def test_levels_not_exist(self):
        # get_option when option name doesn't exist returns None.

        sample_option_name = 'hardcoded_password.doesntexist'
        self.assertIsNone(self.b_config.get_option(sample_option_name))

class TestGetSetting(testtools.TestCase):
    def setUp(self):
        super(TestGetSetting, self).setUp()
        self.b_config = config.BanditConfig(LOG, SAMPLE_CONFIG_FILE)

    def test_not_exist(self):
        # get_setting() when the name doesn't exist returns None

        sample_setting_name = 'doesntexist'
        self.assertIsNone(self.b_config.get_setting(sample_setting_name))
