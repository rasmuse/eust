# -*- coding: utf-8 -*-

from typing import (
    Union,
    )
from pathlib import Path
from tempfile import TemporaryDirectory
import zipfile
import os
import shutil

import pandas as pd

from eust.core import conf, _get_abs_path, _NUTS_DIR, _download_file


_EXCEL_COLS = {
    'COUNTRY': 'country_code',  # In NUTS 2006 file
    'CODE': 'geo',
    'LABEL': 'label',
    'NUTS_LEVEL': 'nuts_level',
    'COUNTRY CODE': 'country_code',  # In NUTS 2010, 2013, 2016 files
    'NUTS CODE': 'geo',
    'NUTS LEVEL': 'nuts_level',
    'NUTS LABEL': 'label'
}

COLS_TO_KEEP = [
    'geo',
    'country_code',
    'nuts_level',
    'label',
    'parent_geo',
]

PARENT_COLNAME = 'parent_geo'


def _read_and_transform_excel_file(excel_path):
    indata = pd.read_excel(excel_path)
    d = indata.reindex(list(_EXCEL_COLS), axis=1).dropna(axis=1, how='all')
    d = d.rename(columns=_EXCEL_COLS)
    parents = d[d.nuts_level > 0].geo.str[0:-1]
    d[PARENT_COLNAME] = parents
    d = d[COLS_TO_KEEP]
    d.set_index('geo', inplace=True)
    d = d.sort_index()
    assert len(d.index) == len(d.index.unique())
    return d


def _read_csv_file(csv_path):
    return pd.read_csv(csv_path, index_col='geo')


_EXCEL_TEMPLATES = ['NUTS_{year}.xlsx', 'NUTS_{year}.xls']
_CSV_TEMPLATE = 'NUTS_{year}.csv'


def _get_nuts_dir():
    return _get_abs_path(_NUTS_DIR)


def _try_read_options(year):
    the_dir = _get_nuts_dir()

    csv_path = the_dir / _CSV_TEMPLATE.format(year=year)
    excel_paths = [
        the_dir / template.format(year=year)
        for template in _EXCEL_TEMPLATES
    ]

    d = None

    try:
        return _read_csv_file(csv_path)
    except FileNotFoundError:
        pass

    for excel_path in excel_paths:
        try:
            d = _read_and_transform_excel_file(excel_path)
            d.to_csv(csv_path)
        except FileNotFoundError:
            pass

    if d is None:
        raise FileNotFoundError(f'no NUTS {year} file found')

    return d


_COUNTRY_NAMES_LANGUAGE = 'English'
_COUNTRY_NAMES_FILENAME = 'country_names.csv'


def read_country_names():
    path = _get_nuts_dir() / _COUNTRY_NAMES_FILENAME
    d = (
        pd.read_csv(path)
        .rename(columns={
            'Code': 'country_code',
            _COUNTRY_NAMES_LANGUAGE: 'country'
            })
        .set_index('country_code')
        ['country']
        )

    return d


def read_nuts_codes(
        year: Union[str, int], drop_extra_regio=False) -> pd.DataFrame:
    d = _try_read_options(year)

    d = d.join(read_country_names(), on='country_code')

    if drop_extra_regio:
        num_countries = len(d.country.unique())
        is_extra_regio = (d.nuts_level > 0) & d.index.str.endswith('Z')
        num_extra_regio = is_extra_regio.sum()
        assert num_extra_regio == 3 * num_countries, num_extra_regio
        d = d[~is_extra_regio]

    return d


def download_nuts_codes():
    rel_subdir = conf['nuts_zip_subdir']
    if not rel_subdir.endswith('/'):
        rel_subdir += '/'

    target_dir = _get_nuts_dir()
    os.makedirs(target_dir, exist_ok=True)
    with TemporaryDirectory() as tempdir:
        tempdir = Path(tempdir)
        zip_path = tempdir / 'archive.zip'
        _download_file(conf['nuts_zip_url'], zip_path)

        archive = zipfile.ZipFile(zip_path)
        if rel_subdir not in archive.namelist():
            raise ValueError(
                f'zip archive does not contain expected subdir {rel_subdir}')

        archive.extractall(path=tempdir)
        temp_subdir = tempdir / rel_subdir
        assert temp_subdir.exists(), list(tempdir.iterdir())

        for src_path in temp_subdir.iterdir():
            relpath = src_path.relative_to(temp_subdir)
            dst_path = target_dir / relpath

            if not dst_path.exists():
                shutil.move(src_path, dst_path)
