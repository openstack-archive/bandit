
paramiko_calls
==============

Description
-----------
Paramiko is a Python library designed to work with the SSH2 protocol for secure
(encrypted and authenticated) connections to remote machines. Bandit reports an
informative issue when it detects the use of Paramiko's "exec_command" or
"invoke_shell" methods advising the user to check inputs. These methods are
used to run the given command strings on a remote host.

Available Since
---------------
 - Bandit v0.12.0

Config Options
--------------
None

Sample Output
-------------
.. code-block:: none

    >> Issue: Probable Paramiko shell execution, check inputs
       Severity: Medium   Confidence: Medium
       Location: ./examples/paramiko_injection.py:4
    3    # this is not safe
    4    paramiko.exec_command('something; reallly; unsafe')
    5

    >> Issue: Probable Paramiko shell execution, check inputs
       Severity: Medium   Confidence: Medium
       Location: ./examples/paramiko_injection.py:10
    9    # this is not safe
    10   SSHClient.invoke_shell('something; bad; here\n')
    11

References
----------

- https://security.openstack.org
- https://github.com/paramiko/paramiko
