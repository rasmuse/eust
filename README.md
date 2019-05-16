# `eust`

A set of tools to download, archive, and read Eurostat data.

[![PyPI package](https://img.shields.io/pypi/v/eust.svg)](https://pypi.python.org/pypi/eust)

## Features

* Read Eurostat tables and metadata as [pandas] datastructures.
* Download tables with one line of code instead of clicking through the [bulk download facility].
* Download, archive, and use multiple table versions. This helps to make your calculations reproducible.
* Python API and command line interface.
* MIT license.

## Bug reports and feature requests

Please [open an issue].

## Documentation

TODO

## Credits

Thanks to the [pandaSDMX] creators for solving the fetching and parsing of metadata.

This package was created with [Cookiecutter] and the [`audreyr/cookiecutter-pypackage`] project template.

[pandas]: https://pandas.pydata.org/
[open an issue]: https://github.com/rasmuse/eust/issues
[bulk download facility]: https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/BulkDownloadListing?sort=1&dir=data
[github repo]: https://github.com/rasmuse/eust
[pandaSDMX]: https://pandasdmx.readthedocs.io
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[`audreyr/cookiecutter-pypackage`]: https://github.com/audreyr/cookiecutter-pypackage
