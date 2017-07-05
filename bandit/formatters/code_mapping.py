# Copyright 2017 Patchman B.V.
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

CODE_MAPPING = {
    'B101': 'assert_used',
    'B102': 'exec_used',
    'B103': 'set_bad_file_permissions',
    'B104': 'hardcoded_bind_all_interfaces',
    'B105': 'hardcoded_password_string',
    'B106': 'hardcoded_password_funcarg',
    'B107': 'hardcoded_password_default',
    'B108': 'hardcoded_tmp_directory',
    'B109': 'password_config_option_not_marked_secret',
    'B110': 'try_except_pass',
    'B111': 'execute_with_run_as_root_equals_true',
    'B112': 'try_except_continue',
    'B201': 'flask_debug_true',
    'B301': 'pickle',
    'B302': 'marshal',
    'B303': 'md5',
    'B304': 'ciphers',
    'B305': 'cipher_modes',
    'B306': 'mktemp_q',
    'B307': 'eval',
    'B308': 'mark_safe',
    'B309': 'httpsconnection',
    'B310': 'urllib_urlopen',
    'B311': 'random',
    'B312': 'telnetlib',
    'B313': 'xml_bad_cElementTree',
    'B314': 'xml_bad_ElementTree',
    'B315': 'xml_bad_expatreader',
    'B316': 'xml_bad_expatbuilder',
    'B317': 'xml_bad_sax',
    'B318': 'xml_bad_minidom',
    'B319': 'xml_bad_pulldom',
    'B320': 'xml_bad_etree',
    'B321': 'ftplib',
    'B322': 'input',
    'B401': 'import_telnetlib',
    'B402': 'import_ftplib',
    'B403': 'import_pickle',
    'B404': 'import_subprocess',
    'B405': 'import_xml_etree',
    'B406': 'import_xml_sax',
    'B407': 'import_xml_expat',
    'B408': 'import_xml_minidom',
    'B409': 'import_xml_pulldom',
    'B410': 'import_lxml',
    'B411': 'import_xmlrpclib',
    'B412': 'import_httpoxy',
    'B501': 'request_with_no_cert_validation',
    'B502': 'ssl_with_bad_version',
    'B503': 'ssl_with_bad_defaults',
    'B504': 'ssl_with_no_version',
    'B505': 'weak_cryptographic_key',
    'B506': 'yaml_load',
    'B601': 'paramiko_calls',
    'B602': 'subprocess_popen_with_shell_equals_true',
    'B603': 'subprocess_without_shell_equals_true',
    'B604': 'any_other_function_with_shell_equals_true',
    'B605': 'start_process_with_a_shell',
    'B606': 'start_process_with_no_shell',
    'B607': 'start_process_with_partial_path',
    'B608': 'hardcoded_sql_expressions',
    'B609': 'linux_commands_wildcard_injection',
    'B701': 'jinja2_autoescape_false',
    'B702': 'use_of_mako_templates'
}
