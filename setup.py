#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('pypi-readme.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'pandas>=0.24',
    'tables>=3.2',
    'pandasdmx>=0.9',
    'requests>=2.5.1',
    'yaconf==0.2',
    'xlrd>=1.0',
    ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Rasmus Einarsson",
    author_email='mr@rasmuseinarsson.se',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A set of tools to download, archive, and read Eurostat data",
    entry_points={
        'console_scripts': [
            'eust=eust.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='eust',
    name='eust',
    packages=find_packages(exclude=('tests')),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rasmuse/eust',
    version='0.4.0',
    zip_safe=False,
)
