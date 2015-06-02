Avoid known week or compromised SSL/TLS versions
=====================
Several well publicized vulnerabilities[0][1] have emerged in versions of
SSL/TLS. It is strongly recommended that software utilizing SSL/TLS for secure
transmissions should avoid the use of these known bad protocol versions.
Developers and deployers wishing to know more should refer to [2].

* Avoid the use of all versions of SSL (versions 2, 3 and before)
* Avoid the use of TLS versions 1.0, 1.1

### Correct
Good version of TLS are defined thusly in Pythons built in ssl module:
- 'PROTOCOL_SSLv23' only in conjunction with 'OP_NO_SSLv2' and 'OP_NO_SSLv3'
- 'PROTOCOL_TLSv1_2'

Good version of TLS are defined thusly in the pyOpenSSL package:
- 'SSLv23_METHOD' only in conjunction with 'OP_NO_SSLv2' and 'OP_NO_SSLv3'
- 'TLSv1_2_METHOD'

### Incorrect
Bad versions of SSL/TLS are defined thusly in Pythons built in ssl module:
- 'PROTOCOL_SSLv2'
- 'PROTOCOL_SSLv3'
- 'PROTOCOL_TLSv1'
- 'PROTOCOL_TLSv1_1'

Bad versions of SSL/TLS are defined thusly in the pyOpenSSL package
- 'SSLv2_METHOD'
- 'SSLv3_METHOD'
- 'TLSv1_METHOD'
- 'TLSv1_1_METHOD'

## Consequences
The following consequences may arise from the use of bad SSL/TLS protocol
versions:

* Unintended data leakage or theft
* System identity impersonation (certificate theft)
* System identity theft (certificate theft)
* Burden caused by mass revocation of compromised certificates

## References
* [0] http://heartbleed.com/
* [1] http://googleonlinesecurity.blogspot.co.uk/2014/10/this-poodle-bites-exploiting-ssl-30.html
* [2] https://security.openstack.org/guidelines/dg_strong-crypto.html
