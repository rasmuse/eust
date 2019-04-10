# -*- coding: utf-8 -*-

from pathlib import Path

import yaconf

APP_NAME = 'eust'

def get_default_config():
    return {
        'download.sdmx_service_name': 'ESTAT',
        'download.sdmx_datastructure_template': 'DSD_{table}',
        'download.bulk_tsv_gz_url_template': (
            'https://ec.europa.eu/eurostat/estat-navtree-portlet-prod/'
            'BulkDownloadListing?sort=1&downfile=data%2F{table}.tsv.gz'
            ),
        'data_dir': '~/eurostat-data',
    }

def modify_config(d):
    d['data_dir'] = Path(d['data_dir']).expanduser()

conf = yaconf.get_file_reader(APP_NAME)
conf.loaders.append(get_default_config)
conf.modify = modify_config
conf.load()
