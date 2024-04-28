#!/usr/bin/env python

"""
Still using setup.py, as I didn't get up to speed with pyproject.toml,
especially due to the workarounds (some quite lame) done to build the .dll.
"""

import os
import sys

from setuptools import find_packages, setup
from setuptools.command.build_ext import build_ext
from setuptools.extension import Library
from wheel.bdist_wheel import bdist_wheel

NAME = "pyzdoc"
if sys.platform[:3].lower() == "win":
    _EXT = ".dll"
    _SUF = "win"
else:
    _EXT = ".so"
    _SUF = "nix"

# Get rid of sysconfig's EXT_SUFFIX (e.g.: .cp310-win_amd64)
class build_dll(build_ext):
    def get_ext_filename(self, ext_name):
        return os.path.join(*ext_name.split(".")) + _EXT


class bdist_wheel_noext(bdist_wheel):
    def get_tag(self):
        return (
            "py3",
            "none",
            self.plat_name.replace("-", "_").replace(".", "_").replace(" ", "_"),
        )


zdoc_dll = Library(
    (NAME + ".zdoc"),
    sources=["pyzdoc/src/zdoc_{:s}.c".format(_SUF)],
    include_dirs=["pyzdoc/src"],
    define_macros=[
        ("UNICODE", None),
        ("_UNICODE", None),
        ("WIN32", None),
        ("_WINDLL", None),
    ],
    extra_link_args=[
        "/DLL",
    ],
    libraries=[
        "user32",
        "kernel32",
    ],
)

setup_args = dict(
    name=NAME,
    version="0.0.0",
    description="A collection of (cool) scripts / utilities",
    author="Cristi Fati",
    author_email="fati_utcluj@yahoo.com",
    maintainer="Cristi Fati",
    maintainer_email="fati_utcluj@yahoo.com",
    classifiers=[
        "Development Status :: 5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development",
        "Typing :: Typed",
    ],
    platforms=["Windows"],
    license="MIT",
    url="https://github.com/CristiFati/pyzdoc",
    download_url="https://pypi.org/project/pyzdoc",
    packages=find_packages(include=["pyzdoc"], exclude=["src", "__pycache__"]),
    cmdclass={
        "build_ext": build_dll,
        "bdist_wheel": bdist_wheel_noext,
    },
    ext_modules=[zdoc_dll],
)

setup(**setup_args)
