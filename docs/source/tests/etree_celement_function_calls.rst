
etree_celement_function_calls
==============================================

Description
-----------
XML vulnerabilities are known and well studied. The defusedxml library provides
a great synopsis of XML vulnerabilities, how they're exploited, and which Python
libraries are vulnerable to which attacks. This plugin test is part of a family
that check for the use of vulnerable XML methods. Specifically this plugin test
looks for calls to:

 - `xml.etree.cElementTree.parse`
 - `xml.etree.cElementTree.iterparse`
 - `xml.etree.cElementTree.fromstring`
 - `xml.etree.cElementTree.XMLParser`

Available Since
---------------
 - Bandit v0.11.0

Config Options
--------------
None

Sample Output
-------------
.. code-block:: none

    >> Issue: Using xml.etree.cElementTree.XMLParser to parse untrusted XML data
    is known to be vulnerable to XML attacks. Replace  xml.etree.cElementTree.XMLParser
    with defusedxml.cElementTree.XMLParser function.
       Severity: High   Confidence: Medium
       Location: ./examples/xml_etree_celementtree.py:11
    10	badET.iterparse('filethatdoesntexist.xml')
    11	a = badET.XMLParser()
    12

References
----------
 - defusedXML - https://pypi.python.org/pypi/defusedxml/
 - __TODO__ : Add XML info to sec best practices, and link here.
