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

import bandit
from bandit.core.test_properties import *


@checks('Call')
def weak_cryptographic_key_size(context):

    DSA_MIN_KEY_SIZE = 2048
    RSA_MIN_KEY_SIZE = 2048

    CRYPTO_DSA_FUNC = ('cryptography.hazmat.primitives.asymmetric.dsa.'
                       'generate_private_key')
    CRYPTO_RSA_FUNC = ('cryptography.hazmat.primitives.asymmetric.rsa.'
                       'generate_private_key')
    PYCRYPTO_DSA_FUNC = 'Crypto.PublicKey.DSA.generate'
    PYCRYPTO_RSA_FUNC = 'Crypto.PublicKey.RSA.generate'

    if context.call_function_name_qual in (CRYPTO_DSA_FUNC, PYCRYPTO_DSA_FUNC):
        if context.get_call_arg_value('key_size') is not None:
            key_size = context.get_call_arg_value('key_size')
        elif context.get_call_arg_value('bits') is not None:
            key_size = context.get_call_arg_value('bits')
        else:
            key_size = context.get_call_arg_at_position(0)

        if key_size < DSA_MIN_KEY_SIZE:
            return bandit.Issue(
                severity=bandit.HIGH,
                confidence=bandit.HIGH,
                text='DSA key sizes below %d bits are considered breakable. '
                     '%s' % (DSA_MIN_KEY_SIZE, context.call_args_string))

    elif context.call_function_name_qual in (CRYPTO_RSA_FUNC, PYCRYPTO_RSA_FUNC):
        if context.get_call_arg_value('key_size') is not None:
            key_size = context.get_call_arg_value('key_size')
        elif context.get_call_arg_value('bits') is not None:
            key_size = context.get_call_arg_value('bits')
        elif context.call_function_name_qual == CRYPTO_RSA_FUNC:
            key_size = context.get_call_arg_at_position(1)
        else:
            key_size = context.get_call_arg_at_position(0)

        if key_size < RSA_MIN_KEY_SIZE:
            return bandit.Issue(
                severity=bandit.HIGH,
                confidence=bandit.HIGH,
                text='RSA key sizes below %d bits are considered breakable. '
                     '%s' % (RSA_MIN_KEY_SIZE, context.call_args_string))
