# FloraTraiter ![Python application](https://github.com/rafelafrance/FloraTraiter/workflows/CI/badge.svg)[![DOI](https://zenodo.org/badge/649758239.svg)](https://zenodo.org/badge/latestdoi/649758239)


Extract traits about plants from authoritative literature.

This repository merges three older repositories:
- `traiter_plants`
- `traiter_efloras`
- `traiter_mimosa`

And I also split some functionality out to enable me to use it in other projects.
- `pdf_parsers`: Scripts for parsing PDFs to prepare them for information extraction.
  - https://github.com/rafelafrance/pdf_parsers
- `LabelTraiter`: Parsing treatments (this repo) and herbarium labels are now separate repositories.
  - https://github.com/rafelafrance/LabelTraiter

I should also mention that this repository builds upon other repositories:
- `common_utils`: This is just a grab bag of simple utilities I used in several other project. I got tired of having to change every repository that used them each time there was an edit, so I just put them here.
  - `https://github.com/rafelafrance/common_utils`
- `spell-well`: Is a super simple "delete-only" spell checker I wrote. There may be better options now, but it survives until I can find one that handles our particular needs.
  - `https://github.com/rafelafrance/spell-well`
- `traiter`: This is the base code for all the rule-based parsers (aka traiters) that I write. The details change but the underlying process is the same for all.
  - `https://github.com/rafelafrance/traiter`

## All right, what's this all about then?
**Challenge**: Extract trait information from plant treatments. That is, if I'm given treatment text like: (Reformatted to emphasize targeted traits.)

![Treatment](assets/treatment.png)

I should be able to extract: (Colors correspond to the text above.)

![Traits](assets/traits.png)

## Terms
Essentially, we are finding relevant terms in the text (NER) and then linking them (Entity Linking). There are several types of terms:
1. The traits themselves: These are things like color, size, shape, woodiness, etc. They are either a measurement, count, or a member of a controlled vocabulary.
2. Plant parts: Things like leaves, branches, roots, seeds, etc. These have traits. So they must be linked to them.
3. Plant subparts: Things like hairs, pores, margins, veins, etc. Leaves can have hairs and so can seeds. They also have traits and will be linked to them, but they must also be linked to a part to have any meaning.
4. Sex: Plants exhibit sexual dimorphism, so we to note which part/subpart/trait notation is associated with which sex.
5. Other text: Things like conjunctions, punctuation, etc. Although they are not recorded, they are often important for parsing and linking of terms.

## Rule-based parsing strategy
1. I label terms using Spacy's phrase and rule-based matchers.
2. Then I match terms using rule-based matchers repeatedly until I have built up a recognizable trait like: color, size, count, etc.
3. Finally, I associate traits with plant parts.

For example, given the text: `Petiole 1-2 cm.`:
- I recognize vocabulary terms like:
    - `Petiole` is plant part
    - `1` a number
    - `-` a dash
    - `2` a number
    - `cm` is a unit notation
- Then I group tokens. For instance:
    - `1-2 cm` is a range with units which becomes a size trait.
- Finally, I associate the size with the plant part `Petiole` by using another pattern matching parser. Spacy will build a labeled sentence dependency tree. We look for patterns in the tree to link traits with plant parts.

There are, of course, complications and subtleties not outlined above, but you should get the gist of what is going on here.

## Install

You will need to have Python3.11+ installed, as well as pip, a package manager for Python.
You can install the requirements into your python environment like so:
```bash
git clone https://github.com/rafelafrance/FloraTraiter.git
cd FloraTraiter
make install
```

Every time you run any script in this repository, you'll have to activate the virtual environment once at the start of your session.

```bash
cd FloraTraiter
source .venv/bin/activate
```

### Extract traits

You'll need some treatment text files. One treatment per file.

Example:

```bash
parse-treatments --treatment-dir /path/to/treatments --json-dir /path/to/output/traits --html-file /path/to/traits.html
```

The output formats --json-dir & --html-file are optional. An example of the HTML output was shown above. An example of JSON output.

```json
{
    "dwc:scientificName": "Astragalus cobrensis A. Gray var. maguirei Kearney, | var. maguirei",
    "dwc:scientificNameAuthorship": "A. Gray | Kearney",
    "dwc:taxonRank": "variety",
    "dwc:dynamicProperties": {
        "fruitPart": "legume",
        "leafPart": "leaflet | leaf",
        "leafletHair": "hair",
        "leafletHairShape": "incurved-ascending",
        "leafletHairSize": "lengthLowInCentimeters: 0.06 ~ lengthHighInCentimeters: 0.08",
        "leafletHairSurface": "pilosulous",
        "legumeColor": "white",
        "legumeSurface": "villosulous",
        "partLocation": "adaxial"
    },
    "text": "..."
}
```

### Taxon database

A taxon database is included with the source code, but it may be out of date. I build a taxon database from 4 sources. The 3 primary sources each have various issues, but they complement each other well.

1. [ITIS sqlite database](https://www.itis.gov/downloads/index.html)
2. [The WFO Plant List](https://wfoplantlist.org/plant-list/classifications)
3. [Plant of the World Online](http://sftp.kew.org/pub/data-repositories/WCVP/)
4. [Some miscellaneous taxa not found in the other sources.](flora/pylib/rules/terms/other_taxa.csv)

Download the first 3 sources and then use the `util_add_taxa.py` script to extract the taxa and put them into a form the parsers can use.

## Tests

There are tests which you can run like so:
```bash
make test
```
