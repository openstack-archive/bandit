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


import bandit
from bandit.core.test_properties import *


@takes_config
@checks('Import', 'ImportFrom')
def blacklist_imports(context, config):
    checks = _load_checks(config)

    # for each check, go through and see if it matches all qualifications
    for check in checks:
        # item 0=import, 1=message, 2=level
        if check[0]:
            for im in check[0]:
                if context.is_module_being_imported(im):
                    return _get_result(check, im)


@takes_config('blacklist_imports')
@checks('Call')
def blacklist_import_func(context, config):
    checks = _load_checks(config)
    if context.call_function_name_qual == '__import__':
        for check in checks:
            # item 0=import, 1=message, 2=level
            if check[0]:
                for im in check[0]:
                    if len(context.call_args) and im == context.call_args[0]:
                        return _get_result(check, im)


def _load_checks(config):
    # load all the checks from the config file
    if config is not None and 'bad_import_sets' in config:
        sets = config['bad_import_sets']
    else:
        sets = []

    checks = []
    for cur_item in sets:
        for blacklist_item in cur_item:
            blacklist_object = cur_item[blacklist_item]
            cur_check = _get_tuple_for_item(blacklist_object)
            # skip bogus checks
            if cur_check:
                checks.append(cur_check)
    return checks


def _get_tuple_for_item(blacklist_object):
    # default values
    imports = None
    message = ""
    level = 'MEDIUM'

    # if the item we got passed isn't a dictionary, do nothing with the object;
    # if the item we got passed doesn't have an imports field, we can't do
    # anything with this.  Return None
    if (not isinstance(blacklist_object, dict) or
            'imports' not in blacklist_object):
        return None

    imports = blacklist_object['imports']

    if 'message' in blacklist_object:
        message = blacklist_object['message']

    if 'level' in blacklist_object:
        if blacklist_object['level'] == 'HIGH':
            level = 'HIGH'
        elif blacklist_object['level'] == 'MEDIUM':
            level = 'MEDIUM'
        elif blacklist_object['level'] == 'LOW':
            level = 'LOW'

    return_tuple = (imports, message, level)
    return return_tuple


def _get_result(check, im):
    # substitute '{module}' for the imported module name
    message = check[1].replace('{module}', im)

    level = None
    if check[2] == 'HIGH':
        level = bandit.HIGH
    elif check[2] == 'MEDIUM':
        level = bandit.MEDIUM
    elif check[2] == 'LOW':
        level = bandit.LOW

    return bandit.Issue(severity=level, confidence=bandit.HIGH, text=message)
