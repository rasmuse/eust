#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `eust` package."""

import pytest

from click.testing import CliRunner
import tempfile
import shutil

import eust
from eust import cli


@pytest.fixture
def temp_repo(request):

    temp_dir = tempfile.mkdtemp()

    def fin():
        shutil.rmtree(temp_dir)

    def temp_dir_conf():
        return {'data_dir': temp_dir}

    eust.conf.loaders.insert(0, temp_dir_conf)
    eust.conf.load()

    request.addfinalizer(fin)

    return temp_dir


def test_nuts_download_and_read(temp_repo):
    with pytest.raises(FileNotFoundError):
        eust.read_nuts_codes(2006)

    with pytest.raises(FileNotFoundError):
        eust.read_nuts_codes('2006')

    eust.download_nuts_codes()

    nc_2006 = eust.read_nuts_codes(2006)

    nc_2006_2 = eust.read_nuts_codes('2006')

    assert nc_2006.shape == nc_2006_2.shape
    assert (nc_2006.stack() == nc_2006_2.stack()).all()


_TEST_TABLE_DOWNLOAD = 'educ_thpar'


def test_table_download_and_read(temp_repo):
    with pytest.raises(FileNotFoundError):
        eust.read_table_data(_TEST_TABLE_DOWNLOAD)

    with pytest.raises(FileNotFoundError):
        eust.read_table_metadata(_TEST_TABLE_DOWNLOAD)

    eust.download_table(_TEST_TABLE_DOWNLOAD)

    metadata = eust.read_table_metadata(_TEST_TABLE_DOWNLOAD)
    data = eust.read_table_data(_TEST_TABLE_DOWNLOAD)

    dims_in_metadata = set(
        metadata['dimensions'].index.unique('dimension'))

    dims_without_metadata = {'time'}

    dims_in_data = set(data.index.names)

    assert dims_in_data <= (dims_in_metadata | dims_without_metadata)


def test_table_read_twice(temp_repo):
    # Read data twice and check that the data is identical;
    # this is relevant since we create the hdf5 format when
    # reading the tsv.gz file the first time.

    eust.download_table(_TEST_TABLE_DOWNLOAD)

    data1 = eust.read_table_data(_TEST_TABLE_DOWNLOAD)
    data2 = eust.read_table_data(_TEST_TABLE_DOWNLOAD)

    assert data1.shape == data2.shape
    assert (data1.stack() == data2.stack()).all()


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
