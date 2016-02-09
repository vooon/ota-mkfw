#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("requirements.txt") as fd:
    requirements = fd.readlines()

setup(
    name='ota-mkfw',
    version='0.0.1',
    description='Simple firmware image packer',
    url='https://github.com/vooon/ota-mkfw',

    author="vladimir Ermakov",
    author_email="vooon341@gmail.com",

    license="Apache-2.0",

    install_requires=requirements,
    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'ota-mkfw=ota_mkfw:main'
        ]
    },
)
