
blacklist_imports
==============================================

Description
-----------
This plugin test is part of a family of tests designed to detect importing of
Python modules with known security implications. Specifically, this this test
looks for modules that appear in a blacklist and are imported using the built
in `import` keyword.


Available Since
---------------
 - Bandit v0.9.0

Config Options
--------------
This plugin test takes configuration block shared with other tests in the same
family, `blacklist_imports`. The configuration provides a list,
`bad_import_sets`, of Python modules that when imported will raise an issue.
Each element of this list provides a Python list of module names, a descriptive
string and a severity level to report.

.. code-block:: yaml

    blacklist_imports:
      bad_import_sets:
          - telnet:
              imports: [telnetlib]
              level: HIGH
              message: "Telnet is considered insecure. Use SSH or some other encrypted protocol."
          - info_libs:
              imports: [pickle, cPickle, subprocess, Crypto]
              level: LOW
              message: "Consider possible security implications associated with {module} module."


Sample Output
-------------
.. code-block:: none

  >> Issue: Telnet is considered insecure. Use SSH or some other encrypted protocol.
     Severity: High   Confidence: High
     Location: ./examples/imports-telnetlib.py:1
  1	import telnetlib
  2	import getpass

References
----------
 - https://security.openstack.org/guidelines/dg_avoid-dangerous-input-parsing-libraries.html
 - https://security.openstack.org/guidelines/dg_use-subprocess-securely.html
