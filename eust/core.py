# -*- coding: utf-8 -*-

import importlib
from typing import (
    Union,
    Optional,
    Sequence,
    )
from pathlib import Path

import yaconf

PathLike = Union[Path, str]

APP_NAME = 'eust'

def get_default_config():
    return {
        'bulk_tsv_page_url_template': (
            'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/'
            'BulkDownloadListing?dir=data&start={letter}'
            ),
        'sdmx_service_name': 'ESTAT',
        'sdmx_datastructure_template': 'DSD_{table}',
        'data_dir': '~/eurostat-data',
    }


def modify_config(d):
    d['data_dir'] = Path(d['data_dir']).expanduser()


conf = yaconf.get_file_reader(APP_NAME)
conf.loaders.append(get_default_config)
conf.modify = modify_config
conf.load()


_TABLES_DIR = 'tables'
_BASE_DIRS = (
    _TABLES_DIR,
    )


def _get_rel_path(*args) -> Path:
    if args:
        base_dir = args[0]
        assert base_dir in _BASE_DIRS, base_dir

    return Path('.').joinpath(*args)


def _get_abs_path(*args) -> Path:
    return conf['data_dir'] / _get_rel_path(*args)


def _list_children(*args) -> Sequence[str]:
    the_parent = _get_abs_path(*args)
    if not the_parent.exists():
        return []
    return sorted([c.name for c in the_parent.iterdir()])
