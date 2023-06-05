# FloraTraiter ![Python application](https://github.com/rafelafrance/FloraTraiter/workflows/CI/badge.svg)
Extract traits about plants from authoritative literature.

This repository merges three older repositories:
- `traiter_plants`
- `traiter_efloras`
- `traiter_mimosa`

More merging for other Traiter repositories for plant traits may occur.

## All right, what's this all about then?
**Challenge**: Extract trait information from plant treatments. That is, if I'm given treatment text like: (Reformatted to emphasize targeted traits.)

![Treatment](assets/treatment.png)

I should be able to extract: (Colors correspond to the text above.)

![Treatment](assets/traits.png)

## Terms
Essentially, we are finding relevant terms in the text (NER) and then linking them (Entity Linking). There are 5 types of terms:
1. The traits themselves: These are things like color, size, shape, woodiness, etc. They are either a measurement, count, or a member of a controlled vocabulary.
2. Plant parts: Things like leaves, branches, roots, seeds, etc. These have traits. So they must be linked to them.
3. Plant subparts: Things like hairs, pores, margins, veins, etc. Leaves can have hairs and so can seeds. They also have traits and will be linked to them, but they must also be linked to a part to have any meaning.
4. Sex: Plants exhibit sexual dimorphism, so we to note which part/subpart/trait notation is associated with which sex.
5. Other text: Things like conjunctions, punctuation, etc. Although they are not recorded, they are often important for parsing and linking of terms.

## Multiple methods for parsing
1. Rule based parsing. Most machine learning models require a substantial training dataset. I use this method to bootstrap the training data. If machine learning methods fail, I can fall back to this.
2. Machine learning models. (In progress)

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
You will need to have Python3.9+ installed, as well as pip, a package manager for Python.
You can install the requirements into your python environment like so:
```bash
git clone https://github.com/rafelafrance/FloraTraiter.git
cd FloraTraiter
python3.9 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip setuptools wheel
python -m pip install .
python -m pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
python -m spacy download en_core_web_sm
```

### Taxon database

A taxon database is included with the source code, but it may be out of date. I build a taxon database from 4 sources. The 3 primary sources each have various issues, but they complement each other well.

1. [ITIS sqlite database](https://www.itis.gov/downloads/index.html)
2. [The WFO Plant List](https://wfoplantlist.org/plant-list/classifications)
3. [Plant of the World Online](http://sftp.kew.org/pub/data-repositories/WCVP/)
4. [Some miscellaneous taxa not found in the other sources.](./flora/pylib/traits/terms/other_taxa.csv)

Download the first 3 sources and then use the `util_add_taxa.py` script to extract the taxa and put them into a form the parsers can use.

## Repository details

### Scripts for parsing PDFs

These scripts extract traits from PDFs containing plant treatments. The PDFs I'm parsing have rather complicated text flows. For example, a single page may jump from a 2-column format to a 1-column format several times in that page. The standard tools for converting PDFs to text were not handing these cases. So I wrote my own scripts to organize text from these documents. The work much better (for our use case) than the standard poppler libraries. _**Note: that these scripts are far from perfect, just better for our use cases.**_ Also note that, we still use the poppler utilities for parsing the PDFs, just not the text assembly part.

#### Main workflow for converting PDFs into text and then extracting traits:

1. [rename_pdfs.py](./flora/rename_pdfs.py) - This is an _**optional**_ step to make working with the PDFs a bit easier. All this utility does is replace problematic characters in a PDF file name (like space, parentheses, etc.) to underscores.
2. [pdf_to_images.py](./flora/pdf_to_images.py)
3. [slice.py](./flora/slice.py) - This script allows you to manually outline text on images from `pdf_to_images.py` with bounding boxes that contain treatment text. The boxes on a page must be in reading order. You need to mark which boxes are at the start of a treatment.
4. [stitch.py](./flora/stitch.py) This script takes the boxes from `slice.py` OCRs them and puts the text into a single output file.
5. [clean_text.py](./flora/clean_text.py) Now we take the text from step 3 and format it so that we can parse the text with spaCy rule-based parsers. This breaks the text into sentences, joins hyphenated words, fixes mojibake, removes control characters, space normalizes text, etc. Examine the output of this text to make sure things are still working as expected.
   1. The step for breaking the text into sentences is very slow.
6. [extract_traits.py](./flora/mimosa_extract_traits.py) Finally, we extract traits from the text using spaCy rule-based parsers.

#### Scripts that may help in PDF parsing projects:

1. [pdf_to_xhtml.py](./flora/pdf_to_xhtml.py) Convert a PDF into an XHTML document that contains the bounding box of every word in the document. This is used to build the pages.
   1. It's just a wrapper around the poppler utility `pdftotext -bbox -nodiag input.pdf output.xhtml`.
2. [xhtml_to_text.py](./flora/xhtml_to_text.py) Assembles the text.
   1. You need to edit the output to remove flow interrupting text such as page headers, footers, figure captions, etc.
   2. We do use margins for cropping pages that can help remove most headers & footers but pages may be skewed, so you should probably check for outliers.
3. [pdf_to_text.py](./flora/images_to_text.py) It tries to directly read text from a PDF. This may work on newer cleaner PDFs. If it works, then you can skip steps 1-4 above and pick up the main flow with `clean_text.py`.
4. [fix_page_nos.py](./flora/fix_page_nos.py) Use this if the images have odd page numbers that make pages out of order.

### Scripts for downloading treatments from eFloras and extracting traits

1. [efloras_downloader.py](./flora/efloras_downloader.py)
2. [efloras_trait_extractor.py](./flora/efloras_trait_extractor.py)

## Tests
There are tests which you can run like so:
```bash
export MOCK_TAXA=1; python -m unittest discover
```

Please `export MOCK_TAXA=0` before you run any scripts on real data.
