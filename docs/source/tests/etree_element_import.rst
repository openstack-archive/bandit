
etree_element_import
==============================================

Description
-----------
XML vulnerabilities are known and well studied. The defusedxml library provides
a great synopsis of XML vulnerabilities, how they're exploited, and which Python
libraries are vulnerable to which attacks. This plugin test is part of a family
that check for the use of vulnerable XML methods. Specifically this plugin test
looks for the module xml.etree.ElementTree being imported.

Available Since
---------------
 - Bandit v0.11.0

Config Options
--------------
None

Sample Output
-------------
.. code-block:: none

  >> Issue: Using xml.etree.ElementTree to parse untrusted XML data is known to
  be vulnerable to XML attacks. Replace xml.etree.ElementTree with defusedxml.ElementTree
  package.
     Severity: Low   Confidence: High
     Location: ./examples/xml_etree_elementtree.py:1
  1	import xml.etree.cElementTree as badET
  2	import defusedxml.cElementTree as goodET

References
----------
- defusedXML - https://pypi.python.org/pypi/defusedxml/
- __TODO__ : Add XML info to sec best practices, and link here.
