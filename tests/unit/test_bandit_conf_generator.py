from bandit.bandit_config_generator import clean_profile
from bandit.bandit_config_generator import disable_checkers
from bandit.bandit_config_generator import tweak_blacklist_calls

import testtools

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

    def test_tweak_blacklist_calls(self):
        config = {
            'profiles': {
                'All': {
                    'include': ['checker1', 'checker2']
                },
            },
            'blacklist_calls': {
                'bad_name_sets' : [
                    {
                        'random': {
                            'qualnames': ['random.random'],
                            'message': 'some message'
                        }
                    },
                    {
                        'telnetlib': {
                            'qualnames': ['telnetlib.*'],
                            'message': 'some message'
                        }
                    }
                ]
            }
        }
        expected_output = {
            'profiles': {
                'All': {
                    'include': ['checker1', 'checker2']
                },
            },
            'blacklist_calls': {
                'bad_name_sets' : [
                    {
                        'telnetlib': {
                            'qualnames': ['telnetlib.*'],
                            'message': 'some message'
                        }
                    }
                ]
            }
        }
        self.assertEqual(tweak_blacklist_calls(config, ['random']),
                         expected_output)
