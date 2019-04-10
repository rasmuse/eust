# -*- coding: utf-8 -*-

import re
import pandas as pd


_DIMENSION_NAME_RE = re.compile(r'^[a-z_]+$')

def _is_valid_dimension_name(s: str) -> bool:
    return bool(_DIMENSION_NAME_RE.match(s))

def _split_values_flags(series: pd.Series) -> pd.DataFrame:
    split = series.str.split(' ')
    df = pd.DataFrame({
        'value': split.apply(lambda l: l[0] if l else None),
        'flag': split.apply(lambda l: l[1] if l and len(l) > 1 else None)
        })
    return df


def read_tsv(path_or_buffer) -> pd.DataFrame:
    d = pd.read_csv(path_or_buffer, sep='\t', header=0, dtype=str)

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

    assert all(map(_is_valid_dimension_name, d.index.names))

    d.index.set_levels(
        [level.str.strip() for level in d.index.levels],
        inplace=True
        )

    d = _split_values_flags(d)

    d.loc[d['value'] == ':', 'value'] = pd.np.nan
    d['value'] = d['value'].astype(float)

    return d
