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


def _iter_table_versions_pairs(latest):
    for table in eust.list_tables():
        versions = eust.list_table_versions(table)
        if latest:
            versions = versions[-1:]

        for version in versions:
            yield (table, version)

@main.command()
@click.option(
    '--versions/--no-versions',
    is_flag=True,
    default=True,
    help='Print version information. (--no-versions implies --latest)',
)
@click.option(
    '--latest',
    is_flag=True,
    default=False,
    help='Print the latest available version only.',
)
def list_tables(versions, latest):
    if not versions:
        latest = True


    for table, version in _iter_table_versions_pairs(latest):
        if not versions:
            click.echo(table)
        else:
            click.echo(f'{table:<20} {version}')


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
