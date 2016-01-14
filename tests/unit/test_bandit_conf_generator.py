# Copyright (c) 2015 VMware, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

import testtools

from bandit.bandit_config_generator import clean_profile
from bandit.bandit_config_generator import disable_checkers


class BanditConfigGeneratorTests(testtools.TestCase):
    def test_clean_profile(self):
        default_config = {
            'profiles': {
                'All': {
                    'include': ['checker1', 'checker2']
                },
                'profile-a': {
                    'include': ['checker3']
                }
            }
        }
        expected_config = {
            'profiles': {
                'profile_name': {
                    'include': ['checker1', 'checker2']
                },
            }
        }
        self.assertEqual(clean_profile(default_config, 'profile_name'),
                         expected_config)

    def test_disable_checkers(self):
        config = {
            'profiles': {
                'All': {
                    'include': ['checker1', 'checker2']
                },
                'profile-a': {
                    'include': ['checker2', 'checker3']
                }
            },
            'checker1': 'additional_config',
            'checker2': 'additional_config'
        }
        expected_output = {
            'profiles': {
                'All': {
                    'include': ['checker1'],
                    'exclude': ['checker2']
                },
                'profile-a': {
                    'include': ['checker3'],
                    'exclude': ['checker2']
                }
            },
            'checker1': 'additional_config'
        }
        self.assertEqual(disable_checkers(config, ['checker2']),
                         expected_output)
