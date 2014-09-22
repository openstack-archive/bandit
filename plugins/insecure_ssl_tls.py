# -*- coding:utf-8 -*-
#
# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import bandit
from bandit.test_selector import *


def get_bad_proto_versions(config):
    ipdb.set_trace()
    bad_ssl_versions = ['PROTOCOL_SSLv2',
                        'PROTOCOL_SSLv23',
                        'SSLv2_METHOD',
                        'SSLv23_METHOD']
    if config is not None and config.ssl.strict_protocol_versions:
        bad_ssl_versions += ['PROTOCOL_SSLv3',
                             'PROTOCOL_TLSv1',
                             'SSLv3_METHOD',
                             'TLSv1_METHOD']
    #if really_strict:
    #    the default is SSLv23, we should moan about that ....
    #    However, it's ok with NO_SSLv2 option added. Also it's
    #    ok if its a client and the server isn't silly.
    #
    return bad_ssl_versions

@takes_config
@checks_functions
def ssl_wrap_with_bad_version(context, config):
    bad_ssl_versions = get_bad_proto_versions(config)
    if (context.call_function_name_qual == 'ssl.wrap_socket'):
        if context.check_call_arg_str_value('ssl_version') in bad_ssl_versions:

            return(bandit.ERROR, 'ssl.wrap_socket call with insecure ssl/tls'
                   ' protocol version identified, security issue.  %s' %
                   context.call_args_string)

@takes_config
@checks_functions
def pyopenssl_wrap_with_bad_version(context, config):
    bad_ssl_versions = get_bad_proto_versions(config)
    if (context.call_function_name_qual == 'SSL.Context'):
        if context.check_call_arg_str_value('method') in bad_ssl_versions:

            return(bandit.ERROR, 'SSL.Context call with insecure ssl/tls'
                   ' protocol version identified, security issue.  %s' %
                   context.call_args_string)

@takes_config
@checks_functions
def any_other_function_with_bad_ssl(context, config):
    bad_ssl_versions = get_bad_proto_versions(config)
    if context.call_function_name_qual != 'ssl.wrap_socket' and \
       context.call_function_name_qual != 'SSL.Context':
        if context.check_call_arg_str_value('method') in bad_ssl_versions or \
           context.check_call_arg_str_value('ssl_version') in bad_ssl_versions:

            return(bandit.WARN, 'Function call with insecure ssl/tls '
                   'protocol identified, possible security issue.  %s' %
                   context.call_args_string)
