# traiter_plants ![Python application](https://github.com/rafelafrance/traiter_plants/workflows/CI/badge.svg)
Extract traits about plants from authoritative literature.

This repository contains rule-based parsers common to various plant parsing projects like:
- [traiter_efloras](https://github.com/rafelafrance/traiter_efloras)
- [traiter_mimosa](https://github.com/rafelafrance/traiter_mimosa)

## Install
You will need to have Python3.10+ installed, as well as pip, a package manager for Python.
You can install the requirements into your python environment like so:
```bash
git clone https://github.com/rafelafrance/traiter_plants.git
cd traiter_plants
make install
```

### Taxon database

I build a taxon database from 5 sources. The 3 primary sources have various issues, but they complement each other very well.

1. [ITIS sqlite database located](https://www.itis.gov/downloads/index.html)
2. [The WFO Plant List](https://wfoplantlist.org/plant-list/classifications)
3. [Plant of the World Online](http://sftp.kew.org/pub/data-repositories/WCVP/)
4. [Some miscellaneous taxa not found in the other sources.](./plants/pylib/vocabulary/other_taxa.csv)

You can use the `add_taxa.py` script to extract the taxa and put them into a form the parsers can use.

## Repository details

## Run
This repository is a library for other Traiter projects and is not run directly.

## Tests
There are tests which you can run like so:
```bash
cd /my/path/to/traiter_plants
export MOCK_TAXA=1; python -m unittest discover
```
