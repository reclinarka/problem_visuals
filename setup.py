#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the chess-problem-visuals library.
# Copyright (C) 2012-2021 Philipp Polland <contact@philipp-polland.dev>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import re
import sys
import textwrap

import setuptools

if sys.version_info < (3,):
    raise ImportError(textwrap.dedent("""\
        You are trying to install chess_problem_visuals on Python 2 but Python 3 is required.

        Consider upgrading to Python 3.
        """))

if sys.version_info < (3, 7):
    raise ImportError("Since version 1.0.0, python-chess requires Python 3.7 or later.")

import problem_visuals as problem_visuals

def read_description():
    """
    Reads the description from README.rst
    """
    with open(os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8") as f:
        description = f.read()

    # Remove doctest comments.
    description = re.sub(r"\s*# doctest:.*", "", description)

    return description


setuptools.setup(
    name="chess_problem_visuals",
    version=problem_visuals.__version__,
    author=problem_visuals.__author__,
    author_email=problem_visuals.__email__,
    description=problem_visuals.__doc__.replace("\n", " ").strip(),
    long_description=read_description(),
    long_description_content_type="text/x-rst",
    license="GPL-3.0+",
    keywords="chess problems visualization",
    url="https://github.com/reclinarka/chess-problem-visuals",
    packages=["chess_problem_visuals"],
    test_suite="test",
    zip_safe=False,  # For mypy
    package_data={
        "chess_problem_visuals": ["py.typed"],
    },
    python_requires=">=3.7",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
