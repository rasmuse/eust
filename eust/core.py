# -*- coding: utf-8 -*-

import importlib
from typing import (
    Union,
    )
from pathlib import Path

import yaconf

PathLike = Union[Path, str]

APP_NAME = 'eust'

def get_default_config():
    return {
        'download.sdmx_service_name': 'ESTAT',
        'download.sdmx_datastructure_template': 'DSD_{table}',
        'download.bulk_tsv_gz_url_template': (
            'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/'
            'BulkDownloadListing?sort=1&downfile=data%2F{table}.tsv.gz'
            ),
        'data_dir': '~/eurostat-data',
        'metadata_formats': [
            'sdmx',
        ],
        'data_formats': [
            'hdf5',
            'tsv_gz',
        ]
    }

def modify_config(d):
    d['data_dir'] = Path(d['data_dir']).expanduser()

conf = yaconf.get_file_reader(APP_NAME)
conf.loaders.append(get_default_config)
conf.modify = modify_config
conf.load()

_PATH_SUFFIXES = {
    'metadata': {
        'sdmx': '.sdmx.xml',
    },
    'data': {
        'tsv_gz': '.tsv.gz',
        'hdf5': '.h5',
    }
}

def get_rel_table_dir(table):
    return Path('tables') / table

def get_rel_table_version_dir(table, version):
    return get_rel_table_dir(table) / version

def list_versions(table):
    table_dir = conf['data_dir'] / get_rel_table_dir(table)
    return sorted(list(table_dir.iterdir()))

def _get_latest_version(table):
    return list_versions(table)[-1]

def _get_best_format(table, version, item):
    preference_order = conf[f'{item}_formats']

    for fmt in preference_order:
        path = conf['data_dir'] / get_rel_item_path(table, version, item, fmt)
        if path.exists():
            return fmt

def get_rel_item_path(table, version, item, fmt):
    suffix = _PATH_SUFFIXES[item][fmt]
    filename = f'{table}{suffix}'
    return get_rel_table_version_dir(table, version) / item / filename

def _read(table, version, item, fmt):
    if version is None:
        version = _get_latest_version(table)

    if fmt is None:
        fmt = _get_best_format(table, version, item)

    read_module = importlib.import_module(f'eust.{item}')
    read_func = getattr(read_module, f'read_{fmt}')
    item_path = conf['data_dir'] / get_rel_item_path(table, version, item, fmt)
    return read_func(item_path)

def read_metadata(table, version=None, fmt=None):
    return _read(table, version, 'metadata', fmt)

def read_data(table, version=None, fmt=None):
    return _read(table, version, 'data', fmt)
