# -*- coding: utf-8 -*-

"""Top-level package for Eurostat tools."""

__author__ = """Rasmus Einarsson"""
__email__ = 'mr@rasmuseinarsson.se'
__version__ = '0.2.0'

from eust.tables import (
    download_table,
    read_table_data,
    read_table_metadata,
    list_tables,
    list_table_versions,
    )

from eust.nuts import (
    read_nuts_codes,
    read_country_names,
    )
