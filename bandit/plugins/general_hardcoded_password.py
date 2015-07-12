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

import os.path
import sys
from appdirs import site_data_dir

import bandit
from bandit.core.test_properties import *


def find_word_list(cfg_word_list_f):
    if type(cfg_word_list_f) == str:
        if "(site_data_dir)" in cfg_word_list_f:
            # We have a substitution to deal with
            site_data_dir_list = site_data_dir("bandit", "",
                                               multipath=True).split(':')
            site_data_dir_list.insert(0, ".")  # Support relative substitution
            for f in site_data_dir_list:
                # check each of the locations for a file
                word_list_f = cfg_word_list_f.replace("(site_data_dir)", f)
                if os.path.isfile(word_list_f):
                    return word_list_f
            logger.error("Could not substitute '(site_data_dir)' "
                         "with a valid word_list file")
            sys.exit(2)

        return cfg_word_list_f  # Return what we were given


@takes_config
@checks('Str')
def hardcoded_password(context, config):
    word_list_file = None
    word_list = []
    # try to read the word list file from config
    if (config is not None and 'word_list' in config):
        word_list_file = find_word_list(config['word_list'])

    # try to open the word list file and read passwords from it
    try:
        f = open(word_list_file, 'r')
    except (OSError, IOError):
        logger.error("Could not open word_list (from config"
                     " file): %s" % word_list_file)
        sys.exit(2)
    else:
        for word in f:
            word_list.append(word.strip())
        f.close()

    # for every password in the list, check against the current string
    for word in word_list:
        if context.string_val and context.string_val == word:
            return bandit.Issue(
                severity=bandit.LOW,
                confidence=bandit.LOW,
                text="Possible hardcoded password '(%s)'" % word
            )
