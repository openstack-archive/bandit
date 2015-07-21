
expatbuilder_import
==============================================

Description
-----------
XML vulnerabilities are known and well studied. The defusedxml library provides
a great synopsis of XML vulnerabilities, how they're exploited, and which Python
libraries are vulnerable to which attacks. This plugin test is part of a family
that check for the use of vulnerable XML methods. Specifically this plugin test
looks for the module `xml.dom.expatbuilder` being imported.

Available Since
---------------
 - Bandit v0.11.0

Config Options
--------------
None

Sample Output
-------------
.. code-block:: none

    >> Issue: Using xml.dom.expatbuilder to parse untrusted XML data is known to
    be vulnerable to XML attacks. Replace xml.dom.expatbuilder with defusedxml.expatbuilder
    package.
       Severity: Low   Confidence: High
       Location: ./examples/xml_expatbuilder.py:1
    1	import xml.dom.expatbuilder as bad
    2	import defusedxml.expatbuilder as good

References
----------
- defusedXML - https://pypi.python.org/pypi/defusedxml/
- __TODO__ : Add XML info to sec best practices, and link here.
