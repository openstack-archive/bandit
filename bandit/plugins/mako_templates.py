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

r"""
Description
-----------
Mako is a Python templating system often used to build web applications. It is
the default templating system used in Pylons and Pyramid. Unlike Jinja2 (an
alternative templating system), Mako has no environment wide variable escaping
mechanism. Because of this, all input variables must be carefully escaped
before use to prevent possible vulnerabilities to Cross Site Scripting (XSS)
attacks.

See also:

- :doc:`jinja2_autoescape_false`.


Config Options
--------------
None

Sample Output
-------------
.. code-block:: none

    >> Issue: Mako templates allow HTML/JS rendering by default and are
    inherently open to XSS attacks. Ensure variables in all templates are
    properly sanitized via the 'n', 'h' or 'x' flags (depending on context).
    For example, to HTML escape the variable 'data' do ${ data |h }.
       Severity: Medium   Confidence: High
       Location: ./examples/mako_templating.py:10
    9
    10  mako.template.Template("hern")
    11  template.Template("hern")


References
----------
- http://www.makotemplates.org/
- https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)
- https://security.openstack.org
- https://security.openstack.org/guidelines/dg_cross-site-scripting-xss.html

.. versionadded:: 0.10.0

"""

import bandit
from bandit.core.test_properties import *


@checks('Call')
def use_of_mako_templates(context):
    # check type just to be safe
    if type(context.call_function_name_qual) == str:
        qualname_list = context.call_function_name_qual.split('.')
        func = qualname_list[-1]
        if 'mako' in qualname_list and func == 'Template':
            # unlike Jinja2, mako does not have a template wide autoescape
            # feature and thus each variable must be carefully sanitized.
            return bandit.Issue(
                severity=bandit.MEDIUM,
                confidence=bandit.HIGH,
                text="Mako templates allow HTML/JS rendering by default and "
                     "are inherently open to XSS attacks. Ensure variables "
                     "in all templates are properly sanitized via the 'n', "
                     "'h' or 'x' flags (depending on context). For example, "
                     "to HTML escape the variable 'data' do ${ data |h }."
            )
