#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as handle:
    LONG_DESCRIPTION = handle.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='perx-webui-testing',
    version='0.1.0',
    description='perx-webui-testing is a test suite which exercises '
                'the UI for Perx Loyalty Management',
    long_description=open('README.md').read(),
    author=u'Omkar Khatavkar',
    url='https://github.com/omkarkhatavkar',
    install_requires=required,
    packages=find_packages(exclude=['tests*']),
)
