
jinja2_autoescape_false
=======================

Description
-----------
Jinja2 is a Python HTML templating system often used to build web applications.
When configuring the Jinja2 environment, the option to use autoescaping on input
can be specificed, by default this is False. With autoescaping enabled, Jinja2
will filter input strings to escape any HTML content that could otherwise
result in the application being vulnerable to Cross Site Scripting (XSS)
attacks.

As the default is false, this plugin test will warn on omission of an autoescape
setting as well as an explicit setting of false. A HIGH severity warning is
generated in either of these scenarios.

Available Since
---------------
 - Bandit v0.10.0

Config Options
--------------
None


Sample Output
-------------

.. code-block:: none

    >> Issue: Using jinja2 templates with autoescape=False is dangerous and can
    lead to XSS. Use autoescape=True to mitigate XSS vulnerabilities.
       Severity: High   Confidence: High
       Location: ./examples/jinja2_templating.py:11
    10  templateEnv = jinja2.Environment(autoescape=False, loader=templateLoader )
    11  Environment(loader=templateLoader,
    12              load=templateLoader,
    13              autoescape=False)
    14

    >> Issue: By default, jinja2 sets autoescape to False. Consider using
    autoescape=True to mitigate XSS vulnerabilities.
       Severity: High   Confidence: High
       Location: ./examples/jinja2_templating.py:15
    14
    15  Environment(loader=templateLoader,
    16              load=templateLoader)
    17


References
----------
- https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)
- https://realpython.com/blog/python/primer-on-jinja-templating/
- http://jinja.pocoo.org/docs/dev/api/#autoescaping
- https://security.openstack.org
