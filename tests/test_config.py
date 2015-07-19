import logging
import mock
import os
import unittest

from appdirs import site_config_dir
from appdirs import user_config_dir

from bandit import bandit

BASE_CONFIG = '/bandit.yaml'
os.environ['XDG_CONFIG_DIRS'] = '/etc:/usr/local/etc'


class ConfigTests(unittest.TestCase):

    def is_current_config(self, arg):
        return arg == self.current_config

    def setUp(self):
        super(ConfigTests, self).setUp()
        # Mock os.path.isfile with one that selectively returns
        # True if location being considered is the present one.
        self.patcher = mock.patch('os.path.isfile')
        self.mocked_isfile = self.patcher.start()
        self.mocked_isfile.side_effect = self.is_current_config

    def tearDown(self):
        self.patcher.stop()

    def test_find_configs(self):
        config_dirs = (['.'] + [user_config_dir("bandit")] +
                       site_config_dir("bandit", multipath=True).split(':'))
        config_locations = [s + BASE_CONFIG for s in config_dirs]

        # check that at least 3 location paths were generated
        self.assertLess(3, len(config_locations))

        # Iterate through found locations
        for c in config_locations:
            self.current_config = c
            ret = bandit._find_config()
            self.assertEquals(self.current_config, ret)

    def test_cannot_find_configs(self):
        self.current_config = "/invalid/file"
        with self.assertRaises(IOError):
            bandit._find_config()
