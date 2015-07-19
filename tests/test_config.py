import logging
import mock
import os
import unittest

from appdirs import site_config_dir
from appdirs import user_config_dir

from bandit.bandit import _find_config as b_find_config
from bandit.bandit import _init_logger as b_init_logger

BASE_CONFIG = '/bandit.yaml'
os.environ['XDG_CONFIG_DIRS'] = '/etc:/usr/local/etc'

log = b_init_logger(debug=True)


class ConfigTests(unittest.TestCase):

    def side_effect(self, arg):
        if arg == self.current_config:
            return True
        else:
            return False

    def setUp(self):
        super(ConfigTests, self).setUp()
        # Mock os.path.isfile with one that selectively returns
        # True if location being considered is the present one.
        patcher = mock.patch('os.path.isfile')
        mock_thing = patcher.start()
        mock_thing.side_effect = self.side_effect

    def tearDown(self):
        pass

    def test_find_configs(self):
        config_dirs = (['.'] + [user_config_dir("bandit")] +
                       site_config_dir("bandit", multipath=True).split(':'))
        config_locations = [s + BASE_CONFIG for s in config_dirs]

        # check that at least >3 locations were currated
        self.assertLess(3, len(config_locations))

        # Iterate through found locations
        for c in config_locations:
            self.current_config = c
            ret = b_find_config(logger=log)
            self.assertEquals(self.current_config, ret)

    def test_cannot_find_configs(self):
        self.current_config = "/invalid/file"
        with self.assertRaises(IOError):
            b_find_config(logger=log)
