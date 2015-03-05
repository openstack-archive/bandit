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


@checks('Call')
def request_with_no_cert_validation(context):
    if (
        'requests' in context.call_function_name_qual and (
            'get' in context.call_function_name or
            'post' in context.call_function_name)
    ):

        if context.check_call_arg_value('verify', 'False'):

            return(bandit.ERROR, 'Requests call with verify=False '
                   'disabling SSL certificate checks, security issue.   %s' %
                   context.call_args_string)
