SHELL:=/bin/bash

.PHONY: setup-env
setup-env:
	pip3 install pipenv
	pipenv install

.PHONY: setup-dev
setup-dev: setup-env
	pipenv install --dev

.PHONY: build
build: setup-env clean
	pipenv run pip install --upgrade setuptools wheel
	python -m setup -q sdist bdist_wheel

.PHONY: install
install: build
	pip install -q ./dist/aws-allowlister*.tar.gz
	aws-allowlister --help

.PHONY: uninstall
uninstall:
	pip uninstall aws-allowlister -y
	pip uninstall -r requirements.txt -y
	pip uninstall -r requirements-dev.txt -y
	pip freeze | xargs pipenv run pip uninstall -y

.PHONY: clean
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*.egg-link' -delete
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +

.PHONY: test
test: setup-dev
	pipenv run bandit -r ./aws_allowlister/
	pipenv run coverage run -m pytest -v

.PHONY: fmt
fmt: setup-dev
	pipenv run black aws_allowlister/

.PHONY: lint
lint: setup-dev
	pipenv run pylint aws_allowlister/

.PHONY: publish
publish: build
	pip install --upgrade twine
	python -m twine upload dist/*
	pip install aws_allowlister

.PHONY: generate-examples
generate-examples: setup-env install
	sh utils/generate_new_scps.sh

.PHONY: update-data
update-data: setup-dev
	pipenv run python utils/update_data.py