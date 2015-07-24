Bandit Test Plugins
===================

Bandit supports many different tests to detect various security issues in
python code. These tests are created as plugins and new ones can be created to
extend the functionality offered by bandit today.

Writing Tests
-------------
To write a test:
 - Identify a vulnerability to build a test for, and create a new file in
   examples/ that contains one or more cases of that vulnerability.
 - Create a new Python source file to contain your test, you can reference
   existing tests for examples.
 - Consider the vulnerability you're testing for, mark the function with one
   or more of the appropriate decorators:

  - @checks('Call')
  - @checks('Import', 'ImportFrom')
  - @checks('Str')

 - Register your plugin using the `bandit.plugins` entry point, see example.
 - The function that you create should take a parameter "context" which is
   an instance of the context class you can query for information about the
   current element being examined.  You can also get the raw AST node for
   more advanced use cases.  Please see the context.py file for more.
 - Extend your Bandit configuration file as needed to support your new test.
 - Execute Bandit against the test file you defined in examples/ and ensure
   that it detects the vulnerability.  Consider variations on how this
   vulnerability might present itself and extend the example file and the test
   function accordingly.


Example Test Plugin
-------------------

.. code-block:: python

    @bandit.checks('Call')
    def prohibit_unsafe_deserialization(context):
        if 'unsafe_load' in context.call_function_name_qual:
            return bandit.Issue(
                severity=bandit.HIGH,
                confidence=bandit.HIGH,
                text="Unsafe deserialization detected."
            )

To register your plugin, you have two options:

1. If you're using setuptools directly, add something like the following to
   your `setup` call::

        # If you have an imaginary bson formatter in the bandit_bson module
        # and a function called `formatter`.
        entry_points={'bandit.formatters': ['bson = bandit_bson:formatter']}
        # Or a check for using mako templates in bandit_mako that
        entry_points={'bandit.plugins': ['mako = bandit_mako']}

2. If you're using pbr, add something like the following to your `setup.cfg`
   file::

        [entry_points]
        bandit.formatters =
            bson = bandit_bson:formatter
        bandit.plugins =
            mako = bandit_mako

Complete Test Plugin Listing
----------------------------

.. toctree::
   :maxdepth: 1

   any_other_function_with_shell_equals_true
   assert_used
   blacklist_calls
   blacklist_import_func
   blacklist_imports
   etree_celement_function_calls
   etree_celement_import
   etree_element_function_calls
   etree_element_import
   exec_used
   execute_with_run_as_root_equals_true
   expatbuilder_function_calls
   expatbuilder_import
   expatreader_function_calls
   expatreader_import
   hardcoded_bind_all_interfaces
   hardcoded_password
   hardcoded_sql_expressions
   hardcoded_tmp_directory
   jinja2_autoescape_false
   linux_commands_wildcard_injection
   lxml_function_calls
   lxml_import
   minidom_function_calls
   minidom_import
   paramiko_calls
   password_config_option_not_marked_secret
   pulldom_function_calls
   pulldom_import
   request_with_no_cert_validation
   sax_function_calls
   sax_import
   set_bad_file_permissions
   ssl_with_bad_defaults
   ssl_with_bad_version
   ssl_with_no_version
   start_process_with_a_shell
   start_process_with_no_shell
   start_process_with_partial_path
   subprocess_popen_with_shell_equals_true
   subprocess_without_shell_equals_true
   try_except_pass
   use_of_mako_templates
   xmlrpclib_import
