# -*- coding: utf-8 -*-

"""Top-level package for Eurostat tools."""

__author__ = """Rasmus Einarsson"""
__email__ = 'mr@rasmuseinarsson.se'
__version__ = '0.1.0'

import pathlib
DATA_DIR = pathlib.Path('~/eurostat/data/data').expanduser()

import eust.tables
import eust.nuts
