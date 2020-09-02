=======
History
=======

0.5.2 (2020-09-02)
------------------

* Add support for pandasdmx v1. (Fixes #7.)


0.5.1 (2020-02-07)
------------------

* Allow numbers in table dimension names.


0.5.0 (2020-02-07)
------------------

* Make table directory names Windows-compatible by writing timestamps without colon. (Fixes issue #4.)
* Test on Python 3.6, 3.7, 3.8.
* Make compatible with pandas v1.0.0.

0.4.0 (2019-05-17)
------------------

* Always sort the index of the data.
* Encode absence of flags as null in flag column.
* Add some config reading functions to API and CLI.
* Write some documentation.


0.3.0 (2019-05-16)
------------------

* Add CLI command list-tables.


0.2.1 (2019-04-29)
------------------

* Fix bug where eust package was not correctly included in distribution.


0.2.0 (2019-04-27)
------------------

* Create download for Eurostat tables and NUTS tables.
* Support only Python 3.6 and 3.7 for now.
* Restructure metadata reader output.
* Create list_tables and list_table_versions functions.
* Transform year-only time index level to integer dtype.
* Change CLI to use new API.
* Implement some tests.


0.1.0 (2019-04-09)
------------------

* First release on PyPI.
