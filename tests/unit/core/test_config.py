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
import unittest

import fixtures
import mock
import testtools

from bandit.core import config


class Test(testtools.TestCase):
    def test_init(self):
        # Can initialize a BanditConfig.

        logger = logging.getLogger('bandit.test')
        cfg_file = os.path.join(os.getcwd(), 'bandit/config/bandit.yaml')
        b_config = config.BanditConfig(logger, cfg_file)

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

        logger = logging.getLogger('bandit.test')
        cfg_file = os.path.join(os.getcwd(), 'notafile')

        m = self.useFixture(
            fixtures.MockPatch('sys.exit', side_effect=Exception)).mock

        self.assertRaises(Exception, config.BanditConfig, logger, cfg_file)

        m.assert_called_once_with(2)

    def test_yaml_invalid(self):
        # When the config yaml file isn't valid, sys.exit(2) is called.

        logger = logging.getLogger('bandit.test')
        cfg_file = os.path.join(os.getcwd(), 'notafile')

        m = self.useFixture(
            fixtures.MockPatch('sys.exit', side_effect=Exception)).mock

        self.assertRaises(Exception, config.BanditConfig, logger, cfg_file)

        m.assert_called_once_with(2)
