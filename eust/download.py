# -*- coding: utf-8 -*-

from tempfile import TemporaryDirectory
import shutil
import os
from pathlib import Path
import datetime
from typing import (
    Mapping,
    Callable,
    Any,
    Optional,
    )

import pandasdmx
import requests
import functools

from eust.core import (
    PathLike,
    conf,
    )


def _write_via_tempdir(
        download_func: Callable[[PathLike], Any],
        dst_path: PathLike
        ) -> None:

    dst_path = Path(dst_path).resolve()
    if dst_path.exists():
        raise FileExistsError(f'the path {dst_path} already exists')

    os.makedirs(dst_path.parent, exist_ok=True)

    with TemporaryDirectory() as td:
        temp_path = Path(td) / dst_path.name
        download_func(temp_path)
        shutil.move(temp_path, dst_path)


def download_metadata_sdmx(table: str, path: PathLike) -> None:
    service = conf['download.sdmx_service_name']
    name = conf['download.sdmx_datastructure_template'].format(table=table)

    def save_datastructure(temp_path):
        r = pandasdmx.Request(service)
        r.datastructure(name).write_source(str(temp_path))

    _write_via_tempdir(save_datastructure, path)


def _download_file(url, path):

    def download_to_path(temp_path):
        r = requests.get(url, stream=True)
        r.raise_for_status()
        with open(temp_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    _write_via_tempdir(download_to_path, path)

def download_data_tsv_gz(table: str, path: PathLike) -> None:
    url = conf['download.bulk_tsv_gz_url_template'].format(table=table)
    _download_file(url, path)


_DOWNLOAD_FORMATS = {
    'metadata': 'sdmx',
    'data': 'tsv_gz',
}

def download_table(table: str, dst_dir: Optional[PathLike] = None) -> None:
    if dst_dir is None:
        date_string = datetime.datetime.utcnow().isoformat()
        dst_dir = conf['data_dir'] / f'tables/{table}/{date_string}'

    dst_dir = Path(dst_dir)

    def download_table(temp_dir):
        for item in ('metadata', 'data'):
            format_name = _DOWNLOAD_FORMATS[item]

            relpath_template = conf[f'{item}_path_templates'][format_name]
            relpath = relpath_template.format(table=table)
            download_path = temp_dir / relpath

            download_func_name = f'download_{item}_{format_name}'
            download_func = globals()[download_func_name]

            download_func(table, download_path)

    _write_via_tempdir(download_table, dst_dir)
