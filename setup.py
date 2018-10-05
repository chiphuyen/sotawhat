#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='sotawhat',
    version='0.0.1',
    packages=['sotawhat'],
    description='SOTA ',
    long_description=str('I often get frustrated searching for the latest '
                         'research results on Google and Arxiv so I wrote '
                         'SOTAwhat, a script to query Arxiv for the latest '
                         'abstracts and extract summaries from them. '),
    url = 'https://huyenchip.com/2018/10/04/sotawhat.html',
    package_data={},
    license="",
    install_requires = ['six', 'nltk', 'PyEnchant']
)
