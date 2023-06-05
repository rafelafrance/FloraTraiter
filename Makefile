.PHONY: test install dev venv clean
.ONESHELL:

VENV=.venv
PYTHON=./$(VENV)/bin/python3.9
PIP_INSTALL=$(PYTHON) -m pip install
SPACY_MODEL=$(PYTHON) -m spacy download en_core_web_sm

test:
	$(PYTHON) -m unittest discover

install: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) .
	$(PIP_INSTALL) git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
	$(SPACY_MODEL)

dev: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) -e .[dev]
	$(PIP_INSTALL) -e ../traiter --config-settings editable_mode=strict
	$(SPACY_MODEL)
	pre-commit install

venv:
	test -d $(VENV) || python3.9 -m venv $(VENV)

clean:
	rm -r $(VENV)
	find -iname "*.pyc" -delete
