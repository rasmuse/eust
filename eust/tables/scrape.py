# -*- coding: utf-8 -*-

import datetime

import requests
import lxml.html

from eust.core import (
    conf,
    )

_PAGE_DATE_FORMAT = r'%d/%m/%Y %H:%M:%S'
_VERSION_DATE_FORMAT = r'%Y-%m-%d %H:%M:%S'


def _get_table_name(row):
    link_text = row.xpath('td')[0].xpath('a')[0].text
    assert link_text.endswith('.tsv.gz'), link_text
    return link_text.replace('.tsv.gz', '')


def _get_dl_url(row):
    return row.xpath('td')[0].xpath('a')[0].attrib['href']


def _get_table_date(row):
    s = row.xpath('td')[3].text
    assert s.startswith(' \xa0')
    return datetime.datetime.strptime(s[2:], _PAGE_DATE_FORMAT)


def _scrape_bulk_infos(initial_letter):
    url_template = conf['bulk_tsv_page_url_template']
    url = url_template.format(letter=initial_letter)
    page = requests.get(url)
    tree = lxml.html.fromstring(page.content)
    rows = tree.xpath('/html/body/div/form/table/tr')
    if not rows:
        raise ValueError('found no rows when scraping bulk download page')
    h0 = rows[0]
    assert h0.xpath('th')[0].xpath('a')[0].text == 'Name', h0
    h1 = rows[1]
    assert h1.xpath('td')[0].xpath('a')[0].text.endswith('up one level'), h1

    table_rows = rows[2:]

    return {
        _get_table_name(r): {
            'version': _get_table_date(r).strftime(_VERSION_DATE_FORMAT),
            'url': _get_dl_url(r)
            }
        for r in table_rows
        }


def _scrape_bulk_info(table):
    table_start_letter = table[0]
    table_infos = _scrape_bulk_infos(table_start_letter)

    if table not in table_infos:
        raise ValueError(f'could not find bulk download info for {table}')

    table_info = table_infos[table]
    return table_info
