#!/usr/bin/env python3
# import tomllib
from distutils.core import setup
from setuptools import find_packages


# def read_pyproject():
#     with open("pyproject.toml", "rb") as in_file:
#         settings = tomllib.load(in_file)
#     return settings


# SETTINGS = read_pyproject()
SETTINGS = {
    "project": {
        "name": "FloraTraiter",
        "version": "1.0.0",
        "description": "",
        "dependencies": [
            "pandas",
            "spacy",
        ],
    },
}


def readme():
    with open("README.md") as in_file:
        return in_file.read()


def license_():
    with open("LICENSE") as in_file:
        return in_file.read()


setup(
    name=SETTINGS["project"]["name"],
    version=SETTINGS["project"]["version"],
    packages=find_packages(),
    install_requires=SETTINGS["project"]["dependencies"],
    include_package_data=True,
    description=SETTINGS["project"]["description"],
    long_description=readme(),
    license=license_(),
    url="https://github.com/rafelafrance/FloraTraiter",
    python_requires=">=3.9",
    scripts=[],
)
