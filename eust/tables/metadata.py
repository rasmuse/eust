# -*- coding: utf-8 -*-

from typing import Mapping

import pandas as pd
import pandasdmx

from eust.core import (
    conf,
    PathLike,
)

# time dimension does not appear in metadata
_EXCLUDED_DIMENSIONS = {"TIME"}


def _is_header_row(d):
    return (d["dimension"] == d["code"]) & (d["dimension"] == d["label"])


def _get_dimensions_0_9(structure_message):
    # pandasdmx v0.9
    codelist = structure_message["codelist"]
    dimensions = (
        codelist[codelist["dim_or_attr"] == "D"]
        .drop(columns="dim_or_attr")
        .reset_index()
        .rename(
            columns={
                "level_0": "dimension",
                "level_1": "code",
                "name": "label",
            }
        )
        .pipe(lambda d: d[~_is_header_row(d)])
        .pipe(lambda d: d.assign(dimension=d.dimension.str.lower()))
        .set_index(["dimension", "code"])
    )

    return dimensions


def _get_dimensions_1(structure_message):
    # pandasdmx v1
    (dsd,) = structure_message.structure.values()  # unpack exactly 1 table
    dimension_names = pandasdmx.to_pandas(dsd.dimensions)

    codelist = pandasdmx.to_pandas(structure_message.codelist)

    dimension_items = {
        name.lower(): codelist[f"CL_{name}"]
        for name in dimension_names
        if name not in _EXCLUDED_DIMENSIONS
    }

    dimensions = (
        pd.concat(dimension_items)
        .rename_axis(["dimension", "code"])
        .rename("label")
        .to_frame()
    )

    return dimensions


def _get_dimensions(codelist):
    if pandasdmx.__version__.startswith("0.9"):
        return _get_dimensions_0_9(codelist)

    if pandasdmx.__version__.startswith("1."):
        return _get_dimensions_1(codelist)

    raise Exception(f"pandasdmx version is {pandasdmx.__version__}")


def _get_attributes_0_9(structure_message):
    # pandasdmx v0.9
    codelist = structure_message["codelist"]
    attributes = (
        codelist[codelist["dim_or_attr"] == "A"]
        .drop(columns="dim_or_attr")
        .reset_index()
        .rename(
            columns={
                "level_0": "attribute",
                "level_1": "code",
                "name": "label",
            }
        )
        .set_index(["attribute", "code"])
    )

    return attributes


def _get_attributes_1(structure_message):
    # pandasdmx v1
    (dsd,) = structure_message.structure.values()  # unpack exactly 1 table
    attribute_names = [attr.id for attr in dsd.attributes]

    codelist = pandasdmx.to_pandas(structure_message.codelist)

    attribute_items = {
        name.lower(): codelist[f"CL_{name}"] for name in attribute_names
    }

    attributes = (
        pd.concat(attribute_items)
        .rename_axis(["attribute", "code"])
        .rename("label")
        .to_frame()
    )

    return attributes


def _get_attributes(structure_message):
    # pandasdmx v1
    if pandasdmx.__version__.startswith("0.9"):
        return _get_attributes_0_9(structure_message)

    if pandasdmx.__version__.startswith("1."):
        return _get_attributes_1(structure_message)

    raise Exception(f"pandasdmx version is {pandasdmx.__version__}")


_SDMX_FILENAME = "metadata.sdmx.xml"


def _download_sdmx(table: str, dst_dir: PathLike) -> None:
    path = dst_dir / _SDMX_FILENAME
    service = conf["sdmx_service_name"]
    name = conf["sdmx_datastructure_template"].format(table=table)

    r = pandasdmx.Request(service)
    r.datastructure(name, tofile=path)


def _read_structure_message(path):
    # Need to support pandasdmx==0.9 because 1.0 is not available for Python3.6
    if pandasdmx.__version__.startswith("0.9"):
        req = pandasdmx.Request()
        structure = req.get(
            fromfile=str(path), writer="pandasdmx.writer.structure2pd"
        )
        return structure.write()

    if pandasdmx.__version__.startswith("1."):
        return pandasdmx.read_sdmx(path)

    raise Exception(f"pandasdmx version is {pandasdmx.__version__}")


def _read(the_dir: PathLike) -> Mapping[str, pd.DataFrame]:
    path = the_dir / _SDMX_FILENAME
    structure_message = _read_structure_message(path)

    result = {
        "dimensions": _get_dimensions(structure_message),
        "attributes": _get_attributes(structure_message),
    }

    return result
