# -*- coding: utf-8 -*-

import eust
import pandas as pd
import re

import eust
import pandas as pd

def _path_code(year):
    return eust.DATA_DIR / f'nuts/codes/NUTS_{year}.csv'

COLS = {
    'COUNTRY': 'country',
    'CODE': 'geo',
    'LABEL': 'label',
    'NUTS_LEVEL': 'nuts_level',
    'COUNTRY CODE': 'country',
    'NUTS CODE': 'geo',
    'NUTS LEVEL': 'nuts_level',
    'NUTS LABEL': 'label'
}

COLS_TO_KEEP = [
    'geo',
    'country',
    'nuts_level',
    'label',
    'parent_geo',
]

PARENT_COLNAME = 'parent_geo'

def _read_and_transform_excel_file(excel_path):
    indata = pd.read_excel(excel_path)
    d = indata.reindex(list(COLS), axis=1).dropna(axis=1, how='all')
    d = d.rename(columns=COLS)
    parents = d[d.nuts_level>0].geo.str[0:-1]
    d[PARENT_COLNAME] = parents
    d = d[COLS_TO_KEEP]
    d.set_index('geo', inplace=True)
    d = d.sort_index()
    assert len(d.index) == len(d.index.unique())
    return d

def load(year, drop_extra_regio=False):
    d = pd.read_csv(_path_code(year), index_col='geo')
    if drop_extra_regio:
        num_countries = len(d.country.unique())
        is_extra_regio = (d.nuts_level > 0) & d.index.str.endswith('Z')
        num_extra_regio = is_extra_regio.sum()
        assert num_extra_regio == 3 * num_countries, num_extra_regio
        d = d[~is_extra_regio]
    return d

def load_country_names(language='English'):
    d = pd.read_csv(eust.DATA_DIR / 'nuts/codes/country_names.csv', sep=';')
    d = d.rename(columns={'Code': 'geo'}).set_index('geo')[language]
    d.name = 'label'
    return d
