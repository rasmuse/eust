# -*- coding: utf-8 -*-


from typing import (
    Sequence,
    )
import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

from eust.core import (
    _TABLES_DIR,
    _get_rel_path,
    _get_abs_path,
    _list_children,
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
        raise FileNotFoundError(f'no versions available of table {table}')
    return versions[-1]


def _read(module, table, version):
    if version is None:
        version = _get_latest_version(table)

    version_dir = _get_table_abs_path(table, version)

    return module._read(version_dir)


def read_table_metadata(table, version=None):
    return _read(eust.tables.metadata, table, version)


def read_table_data(table, version=None):
    return _read(eust.tables.data, table, version)


def download_table(table: str) -> None:
    table_info = _scrape_bulk_info(table)

    version = table_info['version']

    version_dir = _get_table_abs_path(table, version)
    if version_dir.exists():
        return

    with TemporaryDirectory() as td:
        version_tempdir = Path(td) / version
        os.makedirs(version_tempdir)

        eust.tables.metadata._download_sdmx(table, version_tempdir)
        eust.tables.data._download_tsv_gz(table_info['url'], version_tempdir)

        os.makedirs(version_dir.parent, exist_ok=True)
        shutil.move(version_tempdir, version_dir)
