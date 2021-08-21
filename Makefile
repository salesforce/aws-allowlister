SHELL:=/bin/bash

PROJECT := aws-allowlister
PROJECT_UNDERSCORE := aws_allowlister

# ---------------------------------------------------------------------------------------------------------------------
# Environment setup and management
# ---------------------------------------------------------------------------------------------------------------------
setup-env:
	pip3 install pipenv
	pipenv install
setup-dev: setup-env
	pipenv install --dev
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*.egg-link' -delete
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +

# ---------------------------------------------------------------------------------------------------------------------
# Python Testing
# ---------------------------------------------------------------------------------------------------------------------
test: setup-dev
	pipenv run pytest -v
security-test: setup-dev
	pipenv run bandit -r ./${PROJECT_UNDERSCORE}/
fmt: setup-dev
	pipenv run black ${PROJECT_UNDERSCORE}/
lint: setup-dev
	pipenv run pylint ${PROJECT_UNDERSCORE}/

# ---------------------------------------------------------------------------------------------------------------------
# Package building and publishing
# ---------------------------------------------------------------------------------------------------------------------
build: clean setup-env
	python3 -m pip install --upgrade setuptools wheel
	python3 -m setup -q sdist bdist_wheel
install: build
	python3 -m pip install -q ./dist/${PROJECT}*.tar.gz
	${PROJECT} --help
uninstall:
	python3 -m pip uninstall ${PROJECT} -y
	python3 -m pip uninstall -r requirements.txt -y
	python3 -m pip uninstall -r requirements-dev.txt -y
	python3 -m pip freeze | xargs python3 -m pip uninstall -y
publish: build
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*
	python3 -m pip install ${PROJECT}

# ---------------------------------------------------------------------------------------------------------------------
# Miscellaneous development
# ---------------------------------------------------------------------------------------------------------------------
count-loc:
	echo "If you don't have tokei installed, you can install it with 'brew install tokei'"
	echo "Website: https://github.com/XAMPPRocky/tokei#installation'"
	tokei ./*

# ---------------------------------------------------------------------------------------------------------------------
# Repository specific
# ---------------------------------------------------------------------------------------------------------------------
generate-examples: setup-env install
	sh utils/generate_new_scps.sh
update-data: setup-dev
	pipenv run python utils/update_data.py