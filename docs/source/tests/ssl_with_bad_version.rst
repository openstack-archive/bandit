
ssl_with_bad_version
====================

Description
-----------
Several highly publicized [1]_ [2]_, exploitable flaws have been discovered in
all versions of SSL and early versions of TLS. It is strongly recommended that
use of the following known broken protocol versions be avoided:

- SSL v2
- SSL v3
- TLS v1
- TLS v1.1

This plugin test scans for calls to Python methods with parameters that indicate
the used broken SSL/TLS protocol versions. Currently, detection supports methods
using Python's native SSL/TLS support and the pyOpenSSL module. A HIGH severity
warning will be reported whenever known broken protocol versions are detected.

See also:

- :doc:`ssl_with_bad_defaults`.
- :doc:`ssl_with_no_version`.


Available Since
---------------
 - Bandit v0.9.0

Config Options
--------------
.. code-block:: yaml

    ssl_with_bad_version:
        bad_protocol_versions:
            - PROTOCOL_SSLv2
            - SSLv2_METHOD
            - SSLv23_METHOD
            - PROTOCOL_SSLv3  # strict option
            - PROTOCOL_TLSv1  # strict option
            - SSLv3_METHOD    # strict option
            - TLSv1_METHOD    # strict option


Sample Output
-------------
.. code-block:: none

    >> Issue: ssl.wrap_socket call with insecure SSL/TLS protocol version
    identified, security issue.
       Severity: High   Confidence: High
       Location: ./examples/ssl-insecure-version.py:13
    12  # strict tests
    13  ssl.wrap_socket(ssl_version=ssl.PROTOCOL_SSLv3)
    14  ssl.wrap_socket(ssl_version=ssl.PROTOCOL_TLSv1)

References
----------
.. [1] http://heartbleed.com/
.. [2] https://poodlebleed.com/
.. [3] https://security.openstack.org/
