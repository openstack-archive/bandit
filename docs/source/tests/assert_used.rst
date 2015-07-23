
assert_used
==============================================

Description
-----------
This plugin test checks for the use of the Python `assert` keyword. It was
discovered that some projects used assert to enforce interface constraints,
however, assert is removed with compiling to optimised byte code (\*.pyo). This
caused various protections to be removed. The use of assert is also considered
as general bad practice in OpenStack codebases.


Available Since
---------------
 - Bandit v0.11.0

Config Options
--------------
None

Sample Output
-------------
.. code-block:: none

    >> Issue: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code.
       Severity: Low   Confidence: High
       Location: ./examples/assert.py:1
    1	assert True
    2

References
----------
 - https://bugs.launchpad.net/juniperopenstack/+bug/1456193
 - https://bugs.launchpad.net/heat/+bug/1397883
