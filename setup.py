#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("requirements.txt") as fd:
    requirements = fd.readlines()

setup(
    name='otatools',
    version='0.4.0',
    description='Simple firmware image packer',
    url='https://github.com/vooon/ota-mkfw',

    author="vladimir Ermakov",
    author_email="vooon341@gmail.com",

    license="Apache-2.0",

    install_requires=requirements,
    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'ota-mkfw=otatools.mkfw:main',
            'ota-upload=otatools.upload:main',
            'ota-dfu=otatools.dfu:main',
        ]
    },
)
