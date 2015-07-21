
etree_element_function_calls
==============================================

Description
-----------
XML vulnerabilities are known and well studied. The defusedxml library provides
a great synopsis of XML vulnerabilities, how they're exploited, and which Python
libraries are vulnerable to which attacks. This plugin test is part of a family
that check for the use of vulnerable XML methods. Specifically this plugin test
looks for calls to:

 - `xml.etree.ElementTree.parse`
 - `xml.etree.ElementTree.iterparse`
 - `xml.etree.ElementTree.fromstring`
 - `xml.etree.ElementTree.XMLParser`

Available Since
---------------
 - Bandit v0.11.0

Config Options
--------------
None

Sample Output
-------------
.. code-block:: none

  >> Issue: Using xml.etree.ElementTree.XMLParser to parse untrusted XML data is
  known to be vulnerable to XML attacks. Replace xml.etree.ElementTree.XMLParser
  with defusedxml.ElementTree.XMLParser function.
     Severity: High   Confidence: Medium
     Location: ./examples/xml_etree_elementtree.py:11
  10	badET.iterparse('filethatdoesntexist.xml')
  11	a = badET.XMLParser()
  12

References
----------
 - defusedXML - https://pypi.python.org/pypi/defusedxml/
 - __TODO__ : Add XML info to sec best practices, and link here.
