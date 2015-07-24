Configuration
=================================
Bandit is designed to be configurable and cover a wide range of needs, it may
be used as either a local developer utility or as part of a full CI/CD
pipeline. To provide for these various usage scenarios Bandit can be configured
via the 'bandit.yaml' file. Here we can choose the specific test plugins to
run, the test parameters and the desired output report format. These choices
may be grouped into configuration profiles that can be selected at run time.

Upon startup, unless given a specific path via the command line -c option,
Bandit will search for a configuration file in the following locations:

* ./bandit.yaml
* {env_root}/etc/bandit/bandit.yaml
* /usr/local/etc/bandit/bandit.yaml
* ~/.config/bandit/bandit.yaml

Configuring Test Plugins
------------------------
Bandit's configuration file is written in YAML and options for each plugin test
are provided under a section named to match the test method. For example, given
a test plugin called 'try_except_pass' it's configuration section might look
like the following:

.. code-block:: yaml

    try_except_pass:
      check_typed_exception: True

The specific content of the configuration block is determined by the plugin
test itself. See the plugin test list for complete information on configuring
each one.

Test Profiles
-------------
Bandit defaults to running all available test plugins. However, this behavior
can be overridden by grouping tests into named sets, known as profiles, and
specifying a profile using the -p command line option. When running with a
profile only those tests explicitly listed in the chosen profile will be run.
To define a profile set, create a named entry under the 'profiles' section of
the config. For example:

.. code-block:: yaml

    profiles:
      XSS:
        include:
          - jinja2_autoescape_false
          - use_of_mako_templates

      SqlInjection:
        include:
          - hardcoded_sql_expressions

Again, test plugins are referred to using their method name. Thus in the above
example we have created two profiles, 'XSS' and 'SqlInjection' the former
running 'jinja2_autoescape_false' and 'use_of_mako_templates', the later
running just 'hardcoded_sql_expressions'.


Output Report Format
--------------------
In order to integrate with various CI/CD pipelines, Bandit provides a facility
to build pluggable output formatters. A well written formatter should respect
all of the report configuration options given here, however they may also
expose their own specific configuration choices. Please see the complete list
of formatters for details.

Console Output Report Options
-----------------------------
The following options are available to customize the default terminal output
report.

+---------------+------------------------------------------------------------+
| Option        | Description                                                |
+===============+============================================================+
| output_colors | optional terminal escape sequences to display colors,      |
|               |  - DEFAULT: '\\033[0m'                                     |
|               |  - HEADER: '\\033[95m'                                     |
|               |  - LOW: '\\033[94m'                                        |
|               |  - MEDIUM: '\\033[93m'                                     |
|               |  - HIGH: '\\033[91m'                                       |
+---------------+------------------------------------------------------------+


Misc Options
------------

The following miscellaneous options are available:

+---------------------+------------------------------------------------------+
| Option              | Description                                          |
+=====================+======================================================+
| include             | globs of files which should be analyzed,             |
|                     |  - '\*.py'                                           |
|                     |  - '\*.pyw'                                          |
+---------------------+------------------------------------------------------+
| exclude_dirs        | a list of strings, which if found in the path will   |
|                     | cause files to be excluded.                          |
+---------------------+------------------------------------------------------+
| show_progress_every | Optional, show progress every X files.               |
+---------------------+------------------------------------------------------+
| log_format          | Optional, log format string, default:                |
|                     |  - "[%(module)s]\\t%(levelname)s\\t%(message)s"      |
+---------------------+------------------------------------------------------+

Command Line Options
--------------------
usage: bandit [-h] [-r] [-a {file,vuln}] [-n CONTEXT_LINES] [-c CONFIG_FILE]
              [-p PROFILE] [-l] [-f {csv,json,txt,xml}] [-o OUTPUT_FILE] [-v]
              [-d]
              targets [targets ...]

+-----------------------------+----------------------------------------------+
| Option                      | Description                                  |
+=============================+==============================================+
| -h,                         |   show this help message and exit            |
| --help                      |                                              |
+-----------------------------+----------------------------------------------+
| -r,                         |   process files in subdirectories            |
| --recursive                 |                                              |
+-----------------------------+----------------------------------------------+
| -a {file,vuln},             | group results by vulnerability type or file  |
| --aggregate {file,vuln}     | it occurs in                                 |
+-----------------------------+----------------------------------------------+
| -n CONTEXT_LINES,           | max number of code lines to display for each |
| --number CONTEXT_LINES      | issue identified                             |
+-----------------------------+----------------------------------------------+
| -c CONFIG_FILE,             | test config file, defaults to                |
| --configfile CONFIG_FILE    | /etc/bandit/bandit.yaml,                     |
|                             | or./bandit.yaml if not given                 |
+-----------------------------+----------------------------------------------+
| -p PROFILE,                 | test set profile in config to use (defaults  |
| --profile PROFILE           | to all tests)                                |
+-----------------------------+----------------------------------------------+
| -l,                         | results level filter                         |
| --level                     |                                              |
+-----------------------------+----------------------------------------------+
| -f {csv,json,txt,xml},      | specify output format                        |
| --format {csv,json,txt,xml} |                                              |
+-----------------------------+----------------------------------------------+
| -o OUTPUT_FILE,             | write report to filename                     |
| --output OUTPUT_FILE        |                                              |
+-----------------------------+----------------------------------------------+
| -v,                         | show extra information like excluded and     |
| --verbose                   | included files                               |
+-----------------------------+----------------------------------------------+
| -d,                         | turn on debug mode                           |
| --debug                     |                                              |
+-----------------------------+----------------------------------------------+
