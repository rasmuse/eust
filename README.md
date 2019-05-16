# Eurostat tools for Python

A set of tools to download, archive, and read Eurostat data.

[![PyPI package](https://img.shields.io/pypi/v/eust.svg)](https://pypi.python.org/pypi/eust)

# Features

* Read Eurostat tables and metadata as [pandas] datastructures.
* Download whole tables with one line of code instead of clicking through the [bulk download facility].
* Download, archive, and use multiple table versions. This helps to make your calculations reproducible.
* Python API and command line interface.
* MIT license.

# Bug reports and feature requests

Please [open an issue].

# Documentation

## Getting started

Requires Python 3.6+

```bash
pip install eust
```

## Download a table

In Python:

```python
import eust
eust.download_table('apro_cpsh1')  # that's it
```

or on the command line:

```bash
eust download table apro_cpsh1
```

## List available tables

In Python:

```python
my_tables = eust.list_tables()  # returns a list
assert 'apro_cpshr' in my_tables
```

or on the command line:

```bash
eust list-tables  # list all versions of all tables
eust list-tables --latest  # list only the latest version of each table
eust list-tables --no-versions  # list only the table names
```

## Read a table

```python
data = eust.read_table_data('apro_cpsh1')

assert isinstance(data, pandas.DataFrame)
assert list(data.columns) == ['value', 'flag']
```

* The `data` variable is always a [pandas] `DataFrame` with columns `'value'` and `'flag'`.
* This `DataFrame` has a `MultiIndex` with one level per dimension in the dataset.
* The index is fully lexsorted.
* The index values are usually of type `str`. The exception is if a dimension is named `time` and its values looks like years, in which case it is represented as `int`.
* Big tables may take some time to read the first time as they are parsed from Eurostat's `tsv` format. But after the first read they are cached in HDF format which is [much faster to read](http://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#performance-considerations).

```python
assert list(data.index.names) == ['crops', 'strucpro', 'geo', 'time']

data.loc['C1100', :, 'BE', 2017:2018]
```

### Flags

* The `flag` column contains the data flags. It contains `str` values where there are flags, and otherwise `None`. Thus, it is easy to, e.g., extract all the flagged data:

```python
flagged_data = data[data['flag'].notnull()]
```

### Read a specific version

Tables are saved with versions. Simply calling `read_table_data(table_name)` always loads the latest version. To improve reproducibility, pin your code to a specific version:

```python
versions = eust.list_table_versions('apro_cpshr')
latest_version = versions[-1]  # e.g. '2019-05-02 23:00:00'

data = eust.read_table_data('apro_cpsh1', version='2019-05-02 23:00:00')
```

## Read metadata

```python
meta = eust.read_table_data('apro_cpsh1', version='2019-05-02 23:00:00')
assert isinstance(meta, dict)
dimensions = meta['dimensions']
attributes = meta['attributes']
```


## Data locations

`eust` downloads and reads data in a simple directory structure that you can browse and modify as you wish. Adding or removing a table or version just amounts to adding or removing the corresponding directory.

To find out your data directory, do, e.g.:

```python
import eust
eust.conf['data_dir']
```

Or on the command line:

```bash
eust config read data_dir
```

### Importing and exporting data

For now you do this manually. Go to your data directory with your favorite file browser and just copy in or out the relevant directories.

## Configuration

`eust` has a hierarchical configuration reader. In descending order of priority:

* project-specific configuration file (in current working directory)
* user-specific configuration file (in a user folder, e.g., `~/.config/eust/.eustconfig` if you are on Linux)
* default configuration (built into the program)

You can learn your configuration paths either in Python:

```python
import eust
eust.list_config_paths()
```

or on the command line:

```bash
eust config list-paths
```

The config file is a JSON file, so if you want to change the data directory, put a file like this on either of your config paths:

```json
{
    "data_dir": "~/path/to/my-eurostat-data"
}
```

# Credits

Thanks to the [pandaSDMX] creators for solving the fetching and parsing of metadata.

This package was created with [Cookiecutter] and the [`audreyr/cookiecutter-pypackage`] project template.

[pandas]: https://pandas.pydata.org/
[open an issue]: https://github.com/rasmuse/eust/issues
[bulk download facility]: https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&dir=data
[github repo]: https://github.com/rasmuse/eust
[pandaSDMX]: https://pandasdmx.readthedocs.io
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[`audreyr/cookiecutter-pypackage`]: https://github.com/audreyr/cookiecutter-pypackage
