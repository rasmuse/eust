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


def download_metadata(table: str, path: PathLike) -> None:
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

def download_data(table: str, path: PathLike) -> None:
    url = conf['download.bulk_tsv_gz_url_template'].format(table=table)
    _download_file(url, path)


def download_table(table: str, dst_dir: Optional[PathLike] = None) -> None:
    if dst_dir is None:
        date_string = datetime.datetime.utcnow().isoformat()
        dst_dir = conf['data_dir'] / f'tables/{table}/{date_string}/download'

    dst_dir = Path(dst_dir)

    def download_both(temp_dir):
        metadata_path = temp_dir / f'sdmx-structure.xml'
        data_path = temp_dir / f'data.tsv.gz'

        download_metadata(table, metadata_path)
        download_data(table, data_path)

    _write_via_tempdir(download_both, dst_dir)