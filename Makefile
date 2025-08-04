.PHONY: test install dev venv clean activate base
.ONESHELL:

test: activate
	export MOCK_TRAITER=1
	./.venv/bin/python -m unittest discover
	export MOCK_TRAITER=0

install: venv activate base
	./.venv/bin/python -m pip install git+https://github.com/rafelafrance/spell-well.git@main#egg=spell-well
	./.venv/bin/python -m pip install git+https://github.com/rafelafrance/traiter.git@v2.2.3#egg=traiter
	./.venv/bin/python -m pip install .
	./.venv/bin/python -m spacy download en_core_web_md

dev: venv activate base
	./.venv/bin/python -m pip install -e ../../misc/spell-well
	./.venv/bin/python -m pip install -e ../../traiter/traiter
	./.venv/bin/python -m pip install -e .[dev]
	./.venv/bin/python -m spacy download en_core_web_md
	pre-commit install

activate:
	. .venv/bin/activate

base:
	./.venv/bin/python -m pip install -U pip setuptools wheel

venv:
	test -d .venv || python3.11 -m venv .venv

clean:
	rm -r .venv
	find -iname "*.pyc" -delete
