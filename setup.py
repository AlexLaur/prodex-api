# -*- coding: utf-8 -*-
#
# - setup -
#
# Setup of the API.
#
# Copyright (c) 2020 Prodex
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
from setuptools import setup, find_packages


with open("README.md", "r") as f:
    readme = f.read().strip()

with open("LICENSE", "r") as f:
    license = f.read().strip()

setup(
    name='prodex_api',
    version='0.1',
    description='Prodex API python',
    long_description=readme,
    author='Alexandre Laurette',
    url='https://github.com/AlexLaur/prodex-api',
    license=license,
    install_requires=["requests"],
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    zip_safe=False,
)
