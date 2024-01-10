.PHONY: test install dev venv clean setup_subtrees fetch_subtrees
.ONESHELL:

VENV=.venv
PY_VER=python3.11
PYTHON=./$(VENV)/bin/$(PY_VER)
PIP_INSTALL=$(PYTHON) -m pip install
SPACY_MODEL=$(PYTHON) -m spacy download en_core_web_md

test:
	$(PYTHON) -m unittest discover

install: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) .
	$(SPACY_MODEL)

dev: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) -e .[dev]
	$(SPACY_MODEL)
	pre-commit install

venv:
	test -d $(VENV) || $(PY_VER) -m venv $(VENV)

clean:
	rm -r $(VENV)
	find -iname "*.pyc" -delete

setup_subtrees:
	git remote add -f traiter https://github.com/rafelafrance/traiter.git
	git checkout -b upstream/traiter traiter/master
	git subtree split -q --squash --prefix=traiter --annotate='[traiter] ' --rejoin -b merging/traiter
	git checkout main
	git subtree add -q --squash --prefix=traiter merging/traiter

	git remote add -f pdf_parsers https://github.com/rafelafrance/pdf_parsers.git
	git checkout -b upstream/parse pdf_parsers/main
	git subtree split -q --squash --prefix=parse --annotate='[parse] ' --rejoin -b merging/parse
	git checkout main
	git subtree add -q --squash --prefix=parse merging/parse

fetch_subtrees:
	git checkout upstream/traiter
	git pull traiter/master
	git subtree split -q --squash --prefix=traiter --annotate='[traiter] ' --rejoin -b merging/traiter
	git checkout main
	git subtree merge -q --squash --prefix=traiter merging/traiter

	git checkout upstream/parse
	git pull pdf_parsers/main
	git subtree split -q --squash --prefix=parse --annotate='[parse] ' --rejoin -b merging/parse
	git checkout main
	git subtree merge -q --squash --prefix=parse merging/parse
