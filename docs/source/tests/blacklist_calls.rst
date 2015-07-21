
blacklist_calls
==============================================

Description
-----------
Many Python functions have well known security implications. This plugin test
allows these and other methods to be placed into a blacklist. Calls to
to blacklisted functions will be detected and flagged up appropriately. The
default configuration provided with Bandit includes a good list of potentially
dangerous calls.

Available Since
---------------
 - Bandit v0.9.0

Config Options
--------------
This test plugin takes a matching configuration block, `blacklist_calls`. The
configuration block contains a list `bad_name_sets`, each element of which
provides details of a family of potentially dangerous function calls. The call
details include a python list of fully qualified call names, an informative
description and an optional severity level to report if discovered. The default
severity level if not provided is `medium`.

.. code-block:: yaml

    blacklist_calls:
        bad_name_sets:
            - pickle:
                qualnames: [pickle.loads, pickle.load, pickle.Unpickler,
                            cPickle.loads, cPickle.load, cPickle.Unpickler]
                message: "Pickle library appears to be in use, possible security issue."
                level: "HIGH"
            - marshal:
                qualnames: [marshal.load, marshal.loads]
                message: "Deserialization with the marshal module is possibly dangerous."
            - md5:
                qualnames: [hashlib.md5]
                message: "Use of insecure MD5 hash function."
                level: "LOW"


Sample Output
-------------
.. code-block:: none

    >> Issue: Use of unsafe yaml load. Allows instantiation of arbitrary objects. Consider yaml.safe_load().
       Severity: Medium   Confidence: High
       Location: ./examples/yaml_load.py:5
    4	    ystr = yaml.dump({'a' : 1, 'b' : 2, 'c' : 3})
    5	    y = yaml.load(ystr)
    6	    yaml.dump(y)

References
----------
 - See the python documentation
