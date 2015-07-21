
expatbuilder_function_calls
==============================================

Description
-----------
XML vulnerabilities are known and well studied. The defusedxml library provides
a great synopsis of XML vulnerabilities, how they're exploited, and which Python
libraries are vulnerable to which attacks. This plugin test is part of a family
that check for the use of vulnerable XML methods. Specifically this plugin test
looks for calls to:

 - `xml.dom.expatbuilder.parse`
 - `xml.dom.expatbuilder.parseString`

Available Since
---------------
 - Bandit v0.11.0

Config Options
--------------
None


Sample Output
-------------
.. code-block:: none

    >> Issue: Using xml.dom.expatbuilder.parseString to parse untrusted XML data
    is known to be vulnerable to XML attacks. Replace xml.dom.expatbuilder.parseString
    with defusedxml.expatbuilder.parseString function.
       Severity: High   Confidence: Medium
       Location: ./examples/xml_expatbuilder.py:9
    8
    9	bad.parseString(xmlString)
    10	good.parseString(xmlString)

References
----------
- defusedXML - https://pypi.python.org/pypi/defusedxml/
- __TODO__ : Add XML info to sec best practices, and link here.
