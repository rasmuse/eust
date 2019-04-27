# -*- coding: utf-8 -*-

from typing import (
    Mapping,
    )

import pandas as pd
import pandasdmx

from eust.core import (
    conf,
    PathLike,
    )


def _is_header_row(d):
    return (d['dimension'] == d['code']) & (d['dimension'] == d['label'])


def _get_dimensions(codelist):
    dimensions = (
        codelist
        [codelist['dim_or_attr'] == 'D']
        .drop(columns='dim_or_attr')
        .reset_index()
        .rename(columns={
            'level_0': 'dimension',
            'level_1': 'code',
            'name': 'label',
            })
        .pipe(lambda d: d[~_is_header_row(d)])
        .pipe(lambda d: d.assign(dimension=d.dimension.str.lower()))
        .set_index(['dimension', 'code'])
        )

    return dimensions


def _get_attributes(codelist):
    attributes = (
        codelist
        [codelist['dim_or_attr'] == 'A']
        .drop(columns='dim_or_attr')
        .reset_index()
        .rename(columns={
            'level_0': 'attribute',
            'level_1': 'code',
            'name': 'label',
            })
        .set_index(['attribute', 'code'])
        )

    return attributes


_SDMX_FILENAME = 'metadata.sdmx.xml'


def _download_sdmx(table: str, dst_dir: PathLike) -> None:
    path = dst_dir / _SDMX_FILENAME
    service = conf['sdmx_service_name']
    name = conf['sdmx_datastructure_template'].format(table=table)
    r = pandasdmx.Request(service)
    r.datastructure(name).write_source(str(path))


def _read(the_dir: PathLike) -> Mapping[str, pd.DataFrame]:
    path = the_dir / _SDMX_FILENAME
    req = pandasdmx.Request()
    structure = req.get(
        fromfile=str(path),
        writer='pandasdmx.writer.structure2pd'
        )

    codelist = structure.write()['codelist']

    result = {
        'dimensions': _get_dimensions(codelist),
        'attributes': _get_attributes(codelist),
    }

    return result
