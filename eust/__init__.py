# -*- coding: utf-8 -*-

"""Top-level package for Eurostat tools."""

__author__ = """Rasmus Einarsson"""
__email__ = 'mr@rasmuseinarsson.se'
__version__ = '0.2.0'

from eust.core import (
    conf,
    list_versions,
    read_data,
    read_metadata,
    )

from eust.download import (
    download_table,
    )

import eust.nuts
