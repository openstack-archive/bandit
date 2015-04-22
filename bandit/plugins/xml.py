# -*- coding:utf-8 -*-
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
#
# Most of this file is based off of Christian Heimes' work on defusedxml:
#   https://pypi.python.org/pypi/defusedxml/#defusedxml-sax

import bandit
from bandit.core.test_properties import *


###############################################################################
#                             check function calls
###############################################################################
@checks('Call')
def etree_celement_function_calls(context):
    if type(context.call_function_name_qual) == str:
        qlist = context.call_function_name_qual.split('.')
        func = qlist[-1]
        if ('xml' in qlist and 'etree' in qlist and 'cElementTree' in qlist and
                func in ['parse', 'iterparse', 'fromstring', 'XMLParser']):
            s = ("Using xml.etree.cElementTree.%s to parse untrusted XML data"
                 " is known to be vulnerable to XML attacks. Replace "
                 " xml.etree.cElementTree.%s with defusedxml.cElementTree.%s"
                 " function.")
            return(bandit.ERROR, s % (func, func, func))


@checks('Call')
def etree_element_function_calls(context):
    if type(context.call_function_name_qual) == str:
        qlist = context.call_function_name_qual.split('.')
        func = qlist[-1]
        if ('xml' in qlist and 'etree' in qlist and 'ElementTree' in qlist and
                func in ['parse', 'iterparse', 'fromstring', 'XMLParser']):
            s = ("Using xml.etree.ElementTree.%s to parse untrusted XML data"
                 " is known to be vulnerable to XML attacks. Replace"
                 " xml.etree.ElementTree.%s with defusedxml.ElementTree.%s"
                 " function.")
            return(bandit.ERROR, s % (func, func, func))


@checks('Call')
def expatreader_function_calls(context):
    if type(context.call_function_name_qual) == str:
        qlist = context.call_function_name_qual.split('.')
        func = qlist[-1]
        if ('xml' in qlist and 'sax' in qlist and 'expatreader' in qlist and
                func in ['create_parser']):
            s = ("Using xml.sax.expatreader.%s to parse untrusted XML data is"
                 " known to be vulnerable to XML attacks. Replace"
                 " xml.sax.expatreader.%s with defusedxml.expatreader.%s"
                 " function.")
            return(bandit.ERROR, s % (func, func, func))


@checks('Call')
def expatbuilder_function_calls(context):
    if type(context.call_function_name_qual) == str:
        qlist = context.call_function_name_qual.split('.')
        func = qlist[-1]
        if ('xml' in qlist and 'dom' in qlist and 'expatbuilder' in qlist and
                func in ['parse', 'parseString']):
            s = ("Using xml.dom.expatbuilder.%s to parse untrusted XML data"
                 " is known to be vulnerable to XML attacks. Replace"
                 " xml.dom.expatbuilder.%s with defusedxml.expatbuilder.%s"
                 " function.")
            return(bandit.ERROR, s % (func, func, func))


@checks('Call')
def sax_function_calls(context):
    if type(context.call_function_name_qual) == str:
        qlist = context.call_function_name_qual.split('.')
        func = qlist[-1]
        if ('xml' in qlist and 'sax' in qlist and
                func in ['parse', 'parseString', 'make_parser']):
                s = ("Using xml.sax.%s to parse untrusted XML data is known to"
                     " be vulnerable to XML attacks. Replace xml.sax.%s with"
                     " defusedxml.sax.%s function.")
                return(bandit.ERROR, s % (func, func, func))


@checks('Call')
def minidom_function_calls(context):
    if type(context.call_function_name_qual) == str:
        qlist = context.call_function_name_qual.split('.')
        func = qlist[-1]
        if ('xml' in qlist and 'dom' in qlist and 'minidom' in qlist and
                func in ['parse', 'parseString']):
            s = ("Using xml.dom.minidom.%s to parse untrusted XML data is"
                 " known to be vulnerable to XML attacks. Replace"
                 " xml.dom.minidom.%s with defusedxml.minidom.%s"
                 " function.")
            return(bandit.ERROR, s % (func, func, func))


@checks('Call')
def pulldom_function_calls(context):
    if type(context.call_function_name_qual) == str:
        qlist = context.call_function_name_qual.split('.')
        func = qlist[-1]
        if ('xml' in qlist and 'dom' in qlist and 'pulldom' in qlist and
                func in ['parse', 'parseString']):
            s = ("Using xml.dom.pulldom.%s to parse untrusted XML data is"
                 " known to be vulnerable to XML attacks. Replace"
                 " xml.dom.pulldom.%s with defusedxml.pulldom.%s function.")
            return(bandit.ERROR, s % (func, func, func))


@checks('Call')
def lxml_function_calls(context):
    if type(context.call_function_name_qual) == str:
        qlist = context.call_function_name_qual.split('.')
        func = qlist[-1]
        if ('lxml' in qlist and 'etree' in qlist and
                func in ['parse', 'fromstring', 'RestrictedElement',
                         'GlobalParserTLS', 'getDefaultParser',
                         'check_docinfo']):
            s = ("Using lxml.etree.%s to parse untrusted XML data is"
                 " known to be vulnerable to XML attacks. Replace"
                 " lxml.etree.%s with defused.lxml.%s function.")
            return(bandit.ERROR, s % (func, func, func))


###############################################################################
#                                check imports
###############################################################################
@checks('Import', 'ImportFrom')
def etree_celement_import(context):
    if context.is_module_being_imported('xml.etree.cElementTree'):
        s = ("Using xml.etree.cElementTree to parse untrusted XML data is"
             " known to be vulnerable to XML attacks. Replace"
             " xml.etree.cElementTree with defusedxml.cElementTree package.")
        return(bandit.INFO, s)


@checks('Import', 'ImportFrom')
def etree_element_import(context):
    if context.is_module_being_imported('xml.etree.ElementTree'):
        s = ("Using xml.etree.ElementTree to parse untrusted XML data is"
             " known to be vulnerable to XML attacks. Replace"
             " xml.etree.ElementTree with defusedxml.ElementTree package.")
        return(bandit.INFO, s)


@checks('Import', 'ImportFrom')
def expatreader_import(context):
    if context.is_module_being_imported('xml.sax.expatreader'):
        s = ("Using xml.sax.expatreader to parse untrusted XML data is known"
             " to be vulnerable to XML attacks. Replace xml.sax.expatreader"
             " with defusedxml.expatreader package.")
        return(bandit.INFO, s)


@checks('Import', 'ImportFrom')
def sax_import(context):
    if context.is_module_being_imported('xml.sax'):
        s = ("Using xml.sax to parse untrusted XML data is known to be"
             " vulnerable to XML attacks. Replace xml.sax with defusedxml.sax"
             " package.")
        return(bandit.INFO, s)


@checks('Import', 'ImportFrom')
def expatbuilder_import(context):
    if context.is_module_being_imported('xml.dom.expatbuilder'):
        s = ("Using xml.dom.expatbuilder to parse untrusted XML data is known"
             " to be vulnerable to XML attacks. Replace xml.dom.expatbuilder"
             " with defusedxml.expatbuilder package.")
        return(bandit.INFO, s)


@checks('Import', 'ImportFrom')
def minidom_import(context):
    if context.is_module_being_imported('xml.dom.minidom'):
        s = ("Using xml.dom.minidom to parse untrusted XML data is known to be"
             " vulnerable to XML attacks. Replace xml.dom.minidom with"
             " defusedxml.minidom package.")
        return(bandit.INFO, s)


@checks('Import', 'ImportFrom')
def pulldom_import(context):
    if context.is_module_being_imported('xml.dom.pulldom'):
        s = ("Using xml.dom.pulldom to parse untrusted XML data is known to be"
             " vulnerable to XML attacks. Replace xml.dom.pulldom with"
             " defusedxml.pulldom package.")
        return(bandit.INFO, s)


# this one is 'ERROR' instead of 'INFO' because we know the entire package has
# to be monkeypatched via defusedxml.xmlrpc.monkey_patch()
@checks('Import', 'ImportFrom')
def xmlrpclib_import(context):
    if context.is_module_being_imported('xmlrpclib'):
        s = ("Using xmlrpclib to parse untrusted XML data is known to be"
             " vulnerable to XML attacks. Use defused.xmlrpc.monkey_patch()"
             " function to monkey-patch xmlrpclib and mitigate XML"
             " vulnerabilities.")
        return(bandit.ERROR, s)


@checks('Import', 'ImportFrom')
def lxml_import(context):
    if(context.is_module_being_imported('lxml.etree') or
       context.is_module_being_imported('lxml')):
        s = ("Using lxml.etree to parse untrusted XML data is known to be"
             " vulnerable to XML attacks. Replace lxml.etree with"
             " defused.lxml package.")
        return(bandit.INFO, s)
