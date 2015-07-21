
expatreader_function_calls
==============================================

Description
-----------
XML vulnerabilities are known and well studied. The defusedxml library provides
a great synopsis of XML vulnerabilities, how they're exploited, and which Python
libraries are vulnerable to which attacks. This plugin test is part of a family
that check for the use of vulnerable XML methods. Specifically this plugin test
looks for calls to:

 - `xml.sax.expatreader.create_parser`

Available Since
---------------
 - Bandit v0.11.0

Config Options
--------------
None


Sample Output
-------------
.. code-block:: none

    >> Issue: Using xml.sax.expatreader.create_parser to parse untrusted XML data
    is known to be vulnerable to XML attacks. Replace xml.sax.expatreader.create_parser
    with defusedxml.expatreader.create_parser function.
       Severity: High   Confidence: Medium
       Location: ./examples/xml_expatreader.py:4
    3
    4	p = bad.create_parser()
    5	b = good.create_parser()

References
----------
- defusedXML - https://pypi.python.org/pypi/defusedxml/
- __TODO__ : Add XML info to sec best practices, and link here.
