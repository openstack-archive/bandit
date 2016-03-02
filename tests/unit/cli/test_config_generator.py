# -*- coding:utf-8 -*-
#
# Copyright 2016 Hewlett-Packard Enterprise
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

import importlib
import logging

import mock
import testtools
import yaml

from bandit.cli import config_generator
from bandit.core import extension_loader
from bandit.core import test_properties as test


def gen_config(name):
    return {"test": "test data"}


@test.takes_config('test')
@test.checks('Str')
def _test_plugin(context, conf):
    pass


class BanditConfigGeneratorLoggerTests(testtools.TestCase):

    def setUp(self):
        super(BanditConfigGeneratorLoggerTests, self).setUp()
        self.logger = logging.getLogger(config_generator.__name__)
        self.original_logger_handlers = self.logger.handlers
        self.original_logger_level = self.logger.level
        self.logger.handlers = []

    def tearDown(self):
        super(BanditConfigGeneratorLoggerTests, self).tearDown()
        self.logger.handlers = self.original_logger_handlers
        self.logger.level = self.original_logger_level

    def test_init_logger(self):
        # Test that a logger was properly initialized
        config_generator.init_logger()
        self.assertIsNotNone(self.logger)
        self.assertNotEqual([], self.logger.handlers)
        self.assertEqual(logging.INFO, self.logger.level)


class BanditConfigGeneratorTests(testtools.TestCase):
    @mock.patch('sys.argv', ['bandit-config-generator'])
    def test_parse_args_no_defaults(self):
        # Test that the config generator does not show default plugin settings
        return_value = config_generator.parse_args()
        self.assertFalse(return_value.show_defaults)

    @mock.patch('sys.argv', ['bandit-config-generator', '--show-defaults'])
    def test_parse_args_show_defaults(self):
        # Test that the config generator does show default plugin settings
        return_value = config_generator.parse_args()
        self.assertTrue(return_value.show_defaults)

    @mock.patch('sys.argv', ['bandit-config-generator', '--out', 'dummyfile'])
    def test_parse_args_out_file(self):
        # Test config generator get proper output file when specified
        return_value = config_generator.parse_args()
        self.assertEqual('dummyfile', return_value.output_file)

    def test_get_config_settings(self):
        config = {}
        for plugin in extension_loader.MANAGER.plugins:
            function = plugin.plugin
            if hasattr(plugin.plugin, '_takes_config'):
                module = importlib.import_module(function.__module__)
                config[plugin.name] = module.gen_config(
                    function._takes_config)
        settings = config_generator.get_config_settings()
        self.assertEqual(yaml.safe_dump(config), settings)

    @mock.patch('sys.argv', ['bandit-config-generator', '--show-defaults'])
    def test_main_show_defaults(self):
        # Test that the config generator does show defaults and returns 0
        with mock.patch('bandit.cli.config_generator.get_config_settings'
                        ) as mock_config_settings:
            return_value = config_generator.main()
            # The get_config_settings function should have been called
            self.assertTrue(mock_config_settings.called)
            self.assertEqual(0, return_value)
