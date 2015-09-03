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
import uuid

import fixtures
import mock
import testtools

from bandit.core import config


LOG = logging.getLogger('bandit.test')


class TempFile(fixtures.Fixture):
    def __init__(self, contents=None):
        super(TempFile, self).__init__()

        if not contents:
            self.example_key = uuid.uuid4().hex
            self.example_value = uuid.uuid4().hex
            contents = '%s: %s' % (self.example_key, self.example_value)

        self.contents = contents

    def setUp(self):
        super(TempFile, self).setUp()

        with tempfile.NamedTemporaryFile(mode='wt', delete=False) as f:
            f.write(self.contents)

        self.addCleanup(os.unlink, f.name)

        self.name = f.name


class TestInit(testtools.TestCase):
    def test_settings(self):
        # Can initialize a BanditConfig.

        f = self.useFixture(TempFile())
        b_config = config.BanditConfig(LOG, f.name)

        # After initialization, can get settings.
        self.assertEqual(50, b_config.get_setting('progress'))
        self.assertEqual('', b_config.get_setting('color_HEADER'))
        self.assertEqual('', b_config.get_setting('color_DEFAULT'))
        self.assertEqual('', b_config.get_setting('color_LOW'))
        self.assertEqual('', b_config.get_setting('color_MEDIUM'))
        self.assertEqual('', b_config.get_setting('color_HIGH'))
        self.assertEqual('*.py', b_config.get_setting('plugin_name_pattern'))

        self.assertEqual({f.example_key: f.example_value}, b_config.config)
        self.assertEqual(f.example_value, b_config.get_option(f.example_key))

    def test_file_does_not_exist(self):
        # When the config file doesn't exist, sys.exit(2) is called.

        cfg_file = os.path.join(os.getcwd(), 'notafile')

        m = self.useFixture(
            fixtures.MockPatch('sys.exit', side_effect=Exception)).mock

        self.assertRaises(Exception, config.BanditConfig, LOG, cfg_file)

        m.assert_called_once_with(2)

    def test_yaml_invalid(self):
        # When the config yaml file isn't valid, sys.exit(2) is called.

        # The following is invalid because it starts a sequence and doesn't
        # end it.
        invalid_yaml = '- [ something'
        f = self.useFixture(TempFile(invalid_yaml))

        m = self.useFixture(
            fixtures.MockPatch('sys.exit', side_effect=Exception)).mock

        self.assertRaises(Exception, config.BanditConfig, LOG, f.name)

        m.assert_called_once_with(2)

    def test_progress_conf_setting(self):
        # The progress setting can be set in bandit.yaml via
        # show_progress_any.

        example_value = 23
        sample_yaml = 'show_progress_every: %s' % example_value
        f = self.useFixture(TempFile(sample_yaml))

        b_config = config.BanditConfig(LOG, f.name)
        self.assertEqual(example_value, b_config.get_setting('progress'))

    def test_colors_isatty_defaults(self):
        # When stdout says it's a tty there are default colors.

        f = self.useFixture(TempFile())

        self.useFixture(
            fixtures.MockPatch('sys.stdout.isatty', return_value=True))

        b_config = config.BanditConfig(LOG, f.name)

        self.assertEqual('\x1b[95m', b_config.get_setting('color_HEADER'))
        self.assertEqual('\x1b[0m', b_config.get_setting('color_DEFAULT'))
        self.assertEqual('\x1b[94m', b_config.get_setting('color_LOW'))
        self.assertEqual('\x1b[93m', b_config.get_setting('color_MEDIUM'))
        self.assertEqual('\x1b[91m', b_config.get_setting('color_HIGH'))

    def test_colors_isatty_config(self):
        # When stdout says it's a tty the colors can be set in bandit.yaml

        self.useFixture(
            fixtures.MockPatch('sys.stdout.isatty', return_value=True))

        sample_yaml = """
output_colors:
    HEADER: '\\033[23m'
"""
        f = self.useFixture(TempFile(sample_yaml))

        b_config = config.BanditConfig(LOG, f.name)

        self.assertEqual('\x1b[23m', b_config.get_setting('color_HEADER'))


class TestGetOption(testtools.TestCase):
    def setUp(self):
        super(TestGetOption, self).setUp()

        self.example_key = uuid.uuid4().hex
        self.example_subkey = uuid.uuid4().hex
        self.example_subvalue = uuid.uuid4().hex
        sample_yaml = """
%s:
    %s: %s
""" % (self.example_key, self.example_subkey, self.example_subvalue)
        f = self.useFixture(TempFile(sample_yaml))

        self.b_config = config.BanditConfig(LOG, f.name)

    def test_levels(self):
        # get_option with .-separated string.

        sample_option_name = '%s.%s' % (self.example_key, self.example_subkey)
        self.assertEqual(self.example_subvalue,
                         self.b_config.get_option(sample_option_name))

    def test_levels_not_exist(self):
        # get_option when option name doesn't exist returns None.

        sample_option_name = '%s.%s' % (uuid.uuid4().hex, uuid.uuid4().hex)
        self.assertIsNone(self.b_config.get_option(sample_option_name))


class TestGetSetting(testtools.TestCase):
    def setUp(self):
        super(TestGetSetting, self).setUp()
        f = self.useFixture(TempFile())
        self.b_config = config.BanditConfig(LOG, f.name)

    def test_not_exist(self):
        # get_setting() when the name doesn't exist returns None

        sample_setting_name = uuid.uuid4().hex
        self.assertIsNone(self.b_config.get_setting(sample_setting_name))
