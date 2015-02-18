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
import constants
import ast


def risk(func, risk):
    ''' Decorator function to set 'risk' attribute '''
    if risk not in constants.RISK:
        raise TypeError("Risk error: %s is not one of %s." % (risk,
                        ",".join(constants.RISK)))
    func._risk = risk
    return func


def confidence(func, conf):
    ''' Decorator function to set 'severity' attribute '''
    if conf not in constants.CONFIDENCE:
        raise TypeError("Confidence error: %s is not one of %s." % (conf,
                        ",".join(constants.CONFIDENCE)))
    func._severity = conf
    return func


def category(func, category):
    ''' Decorator function to set 'category' '''
    if category not in constants.CATEGORIES:
        raise TypeError("Category error: %s is not one of %s." % (category,
                        ",".join(constants.CATEGORIES)))


def title(func, title):
    ''' Decorator function to set 'title' attribute '''
    func._title = title
    return func


def uuid(func, uuid):
    ''' Decorator function to set 'uuid' attribute '''
    func._id = uuid
    return func


def checks(func, *args):
    ''' Decorator function to set type of checks to be run
    '''
    if not hasattr(func, "_checks"):
        func._checks = []
    for a in args:
        holder = getattr(ast, a)
        if holder and issubclass(holder, ast.stmt):
            func._checks.append(a)
        else:
            raise TypeError("NodeType Error: %s is not a valid node type within AST" % a)
    return func


def checks_functions(func):
    '''Test function checks function definitions

    Use of this delegate before a test function indicates that it should be
    called any time a function definition is encountered.
    '''
    if not hasattr(func, "_checks"):
        func._checks = []
    func._checks.append("functions")
    return func


def checks_calls(func):
    '''Test function checks function calls

    Use of this delegate before a test function indicates that it should be
    called any time a function call is encountered.
    '''
    if not hasattr(func, "_checks"):
        func._checks = []
    func._checks.append("calls")
    return func


def checks_imports(func):
    '''Test function checks imports

    Use of this delegate before a test function indicates that it should be
    called any time an import is encountered.
    '''
    if not hasattr(func, "_checks"):
        func._checks = []
    func._checks.append("imports")
    return func


def checks_strings(func):
    '''Test function checks strings

    Use of this delegate before a test function indicates that it should be
    called any time a string value is encountered.
    '''
    if not hasattr(func, "_checks"):
        func._checks = []
    func._checks.append("strings")
    return func


def checks_exec(func):
    '''Test function checks exec nodes

    Use of this delegate before a test function indicates that it should be
    called any time the 'exec' statement is encountered.
    '''
    if not hasattr(func, "_checks"):
        func._checks = []
    func._checks.append("exec")
    return func


def takes_config(*args):
    '''Test function takes config

    Use of this delegate before a test function indicates that it should be
    passed data from the config file. Passing a name parameter allows
    aliasing tests and thus sharing config options.
    '''
    name = ""

    def _takes_config(func):
        if not hasattr(func, "_takes_config"):
            func._takes_config = name
        return func

    if len(args) == 1 and callable(args[0]):
        name = args[0].__name__
        return _takes_config(args[0])
    else:
        name = args[0]
        return _takes_config
