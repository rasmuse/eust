# -*- coding: utf-8 -*-

"""Console script for eust."""
import sys
import click
import eust


@click.group()
def main():
    pass


@main.group()
def download():
    pass


@download.command()
@click.argument('tables', type=str, nargs=-1)
def table(tables):
    for table in tables:
        eust.download_table(table)


@download.command()
def nuts_codes():
    eust.download_nuts_codes()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
