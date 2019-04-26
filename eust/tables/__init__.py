# -*- coding: utf-8 -*-


from typing import (
    Sequence,
    )
import importlib
import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from eust.core import (
    _TABLES_DIR,
    _get_rel_path,
    _get_abs_path,
    _list_children,
    conf,
    )
from eust.tables.scrape import _scrape_bulk_info
import eust.tables.metadata
import eust.tables.data


def _get_table_rel_path(*args):
    return _get_rel_path(_TABLES_DIR, *args)


def _get_table_abs_path(*args):
    return _get_abs_path(_TABLES_DIR, *args)


def list_tables() -> Sequence[str]:
    return _list_children(_TABLES_DIR)


def list_table_versions(table) -> Sequence[str]:
    return _list_children(_TABLES_DIR, table)


def _get_latest_version(table) -> str:
    versions = list_table_versions(table)
    if not versions:
        raise ValueError(f'no versions available of table {table}')
    return versions[-1]


def _list_formats(table, version, item):
    return _list_children(_TABLES_DIR, table, version, item)


def _get_best_format(table, version, item) -> str:
    formats = _list_formats(table, version, item)
    if not formats:
        raise ValueError(f'no formats available of table {table} {item}')

    priority_list = conf[f'table_{item}_formats']

    for format_ in priority_list:
        if format_ in formats:
            return format_

    raise ValueError(f'none of the formats {formats} in {priority_list}')


def _read_table_item(table, version, item, fmt):
    if version is None:
        version = _get_latest_version(table)

    if fmt is None:
        fmt = _get_best_format(table, version, item)

    item_path = _get_table_abs_path(table, version, item, fmt)

    read_module = importlib.import_module(f'eust.tables.{item}')
    read_func = getattr(read_module, f'read_{fmt}')
    return read_func(item_path)


def read_table_metadata(table, version=None, fmt=None):
    return _read_table_item(table, version, 'metadata', fmt)


def read_table_data(table, version=None, fmt=None):
    return _read_table_item(table, version, 'data', fmt)


def download_table(table: str) -> None:
    table_info = _scrape_bulk_info(table)

    version = table_info['version']

    version_dir = _get_table_abs_path(table, version)
    if version_dir.exists():
        return

    with TemporaryDirectory() as td:
        sdmx_relpath = _get_table_rel_path(table, version, 'metadata', 'sdmx')
        tsv_gz_relpath = _get_table_rel_path(table, version, 'data', 'tsv_gz')

        sdmx_tempdir = Path(td) / sdmx_relpath
        tsv_gz_tempdir = Path(td) / tsv_gz_relpath

        os.makedirs(sdmx_tempdir)
        os.makedirs(tsv_gz_tempdir)

        eust.tables.metadata.download_sdmx(table, sdmx_tempdir)
        eust.tables.data.download_tsv_gz(
            table,
            tsv_gz_tempdir,
            url=table_info['url']
            )

        version_tempdir = Path(td) / _get_table_rel_path(table, version)
        shutil.move(version_tempdir, version_dir)
