# -*- coding: utf-8 -*-

import eust
import pandas as pd
import re

def read_labels(structure_path):
    req = pandasdmx.Request()
    structure = req.get(
        fromfile=structure_path,
        writer='pandasdmx.writer.structure2pd'
        )
    codelist = structure.write()['codelist']

    result = {}

    dims = codelist[codelist['dim_or_attr']=='D'].groupby(level=0)
    for dim, dim_metadata in dims:
        key = f'dimension/{dim}'
        labels = dim_metadata.loc[dim]['name']
        labels.index.name = 'code'
        result[key] = labels

    attrs = codelist[codelist['dim_or_attr']=='A'].groupby(level=0)
    for attr, attr_metadata in attrs:
        key = f'attr/{attr}'
        labels = attr_metadata.loc[attr]['name']
        labels.index.name = 'code'
        result[key] = labels

    return result

dimension_name_re = re.compile(r'[a-z_]+')

def valid_dimension_name(s):
    return dimension_name_re.match(s)

def split_values_flags(series):
    split = series.str.split(' ')
    df = pd.DataFrame({
        'value': split.apply(lambda l: l[0] if l else None),
        'flag': split.apply(lambda l: l[1] if l and len(l) > 1 else None)
        })
    return df

def raw_to_dataframe(path):
    d = pd.read_csv(path, sep='\t', header=0, dtype=str)

    top_left_cell = d.columns[0]

    row_dimension_names, header_dimension_name = top_left_cell.split('\\')
    row_dimension_names = row_dimension_names.split(',')
    index_data = d[top_left_cell]
    del d[top_left_cell]
    assert len(set(index_data)) == len(index_data) # no duplicates


    assert len(row_dimension_names) >= 1

    d.columns.name = header_dimension_name

    index_data = index_data.apply(lambda s: s.split(','))

    d.index = pd.MultiIndex.from_arrays(
        list(zip(*index_data)),
        names=row_dimension_names
        )

    # cannot handle multidimensional column labels
    d = d.stack()

    assert set(d.apply(type)) == {str}
    assert isinstance(d, pd.Series), d.columns

    assert all(map(valid_dimension_name, d.index.names))

    d.index.set_levels(
        [level.str.strip() for level in d.index.levels],
        inplace=True
        )

    d = split_values_flags(d)

    d.loc[d['value'] == ':', 'value'] = pd.np.nan
    d['value'] = d['value'].astype(float)

    return d

def _hdf_path(table_name):
    return eust.DATA_DIR / f'tables/{table_name}.h5'

def load(table_name, key='data'):
    d = pd.read_hdf(_hdf_path(table_name), key)
    if key == 'data':
        d['flag'] = d['flag'].replace({'': None})
    return d

def _is_meta(key):
    return key.startswith('/labels')

def load_meta(table_name):
    with pd.HDFStore(_hdf_path(table_name)) as store:
        return {
            k: store[k]
            for k in store.keys()
            if _is_meta(k)
            }
