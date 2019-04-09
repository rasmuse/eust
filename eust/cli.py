# -*- coding: utf-8 -*-

"""Console script for eust."""
import sys
import click
import eust

@click.group()
def main():
    pass

@main.group()
def nuts():
    pass

@nuts.command()
@click.argument('excel_file', type=click.Path(exists=True))
@click.argument('outfile', type=click.Path(exists=False))
def to_csv(excel_file, outfile):
    import eust.nuts
    d = eust.nuts._read_and_transform_excel_file(excel_file)
    d.to_csv(outfile)


@main.group()
def table():
    pass

@table.command()
@click.argument('table_name', type=str)
@click.argument('outfile', type=click.Path(exists=False))
def download_datastructure(table_name, outfile):
    import eust.metadata
    eust.metadata.download_datastructure(table_name, outfile)


@table.command()
@click.argument('structure_file', type=click.Path(exists=True))
@click.argument('tsv_file', type=click.Path(exists=True))
@click.argument('hdf_file', type=click.Path(exists=False))
def create(structure_file, tsv_file, hdf_file):
    import pandas as pd
    import eust.tables
    import eust.metadata

    with pd.HDFStore(hdf_file) as store:
        store['data'] = eust.tables.raw_to_dataframe(tsv_file)
        for key, labels in eust.metadata.read_labels(structure_file).items():
            store[f'labels/{key}'] = labels


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
