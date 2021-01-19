SHELL:=/bin/bash

.PHONY: setup_env
setup_env:
	python3 -m venv ./venv && source venv/bin/activate
	python -m pip install -r requirements.txt

.PHONY: setup_dev
setup_dev: setup_env
	python -m pip install -r requirements-dev.txt

.PHONY: build
build: setup_env clean
	python -m pip install --upgrade setuptools wheel
	python -m setup -q sdist bdist_wheel

.PHONY: install
install: build
	python -m pip install -q ./dist/aws-allowlister*.tar.gz
	aws-allowlister --help

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
test:
	bandit -r ./aws_allowlister/
	python -m coverage run -m pytest -v

.PHONY: fmt
fmt: setup_dev
	black aws_allowlister/

.PHONY: lint
lint: setup_dev
	pylint aws_allowlister/
