#!/usr/bin/env bash
set -ex

make uninstall
#pip install aws-allowlister
make install

# Check that it runs without error
aws-allowlister --help
aws-allowlister --version

# Get the latest tag
#git fetch origin
#latest_version=$(git describe --tags `git rev-list --tags --max-count=1`)
export prefix="aws-allowlister, version "
export latest_version=`aws-allowlister --version | sed -e "s/^$prefix//"`
echo "latest version: $latest_version"
export LATEST_VERSION=$latest_version
mkdir -p examples/${LATEST_VERSION}/
mkdir -p examples/latest/

# Create directory if it does not exist, then write the SCP to that path specific to the version
# Also update it to a "latest" folder, that way we can view the diff in commits.
# All (includes FedRAMP)
echo "examples/$LATEST_VERSION/All-AllowList-SCP.json"
aws-allowlister generate --quiet > examples/${LATEST_VERSION}/All-AllowList-SCP.json
aws-allowlister generate --quiet > examples/latest/All-AllowList-SCP.json
aws-allowlister generate --quiet --table > examples/${LATEST_VERSION}/All-AllowList-SCP.md
aws-allowlister generate --quiet --table > examples/latest/All-AllowList-SCP.md
# All Commercial (does not include FedRAMP)
aws-allowlister generate -sphi --quiet > examples/${LATEST_VERSION}/Commercial-AllowList-SCP.json
aws-allowlister generate -sphi --quiet > examples/latest/Commercial-AllowList-SCP.json
aws-allowlister generate -sphi --quiet --table > examples/${LATEST_VERSION}/Commercial-AllowList-SCP.md
aws-allowlister generate -sphi --quiet --table > examples/latest/Commercial-AllowList-SCP.md
# SOC
aws-allowlister generate -s --quiet > examples/${LATEST_VERSION}/SOC-AllowList-SCP.json
aws-allowlister generate -s --quiet > examples/latest/SOC-AllowList-SCP.json
aws-allowlister generate -s --quiet --table > examples/${LATEST_VERSION}/SOC-AllowList-SCP.md
aws-allowlister generate -s --quiet --table > examples/latest/SOC-AllowList-SCP.md
# PCI
aws-allowlister generate -p --quiet > examples/${LATEST_VERSION}/PCI-AllowList-SCP.json
aws-allowlister generate -p --quiet > examples/latest/PCI-AllowList-SCP.json
aws-allowlister generate -p --quiet --table > examples/${LATEST_VERSION}/PCI-AllowList-SCP.md
aws-allowlister generate -p --quiet --table > examples/latest/PCI-AllowList-SCP.md
# HIPAA
aws-allowlister generate -h --quiet > examples/${LATEST_VERSION}/HIPAA-AllowList-SCP.json
aws-allowlister generate -h --quiet > examples/latest/HIPAA-AllowList-SCP.json
aws-allowlister generate -h --quiet --table > examples/${LATEST_VERSION}/HIPAA-AllowList-SCP.md
aws-allowlister generate -h --quiet --table > examples/latest/HIPAA-AllowList-SCP.md
# ISO
aws-allowlister generate -i --quiet > examples/${LATEST_VERSION}/ISO-AllowList-SCP.json
aws-allowlister generate -i --quiet > examples/latest/ISO-AllowList-SCP.json
aws-allowlister generate -i --quiet --table > examples/${LATEST_VERSION}/ISO-AllowList-SCP.md
aws-allowlister generate -i --quiet --table > examples/latest/ISO-AllowList-SCP.md
# FedRAMP High
aws-allowlister generate -fh --quiet > examples/${LATEST_VERSION}/FedRAMP_High-AllowList-SCP.json
aws-allowlister generate -fh --quiet > examples/latest/FedRAMP_High-AllowList-SCP.json
aws-allowlister generate -fh --quiet --table > examples/${LATEST_VERSION}/FedRAMP_High-AllowList-SCP.md
aws-allowlister generate -fh --quiet --table > examples/latest/FedRAMP_High-AllowList-SCP.md
# FedRAMP Moderate
aws-allowlister generate -fm --quiet > examples/${LATEST_VERSION}/FedRAMP_Moderate-AllowList-SCP.json
aws-allowlister generate -fm --quiet > examples/latest/FedRAMP_Moderate-AllowList-SCP.json
aws-allowlister generate -fm --quiet --table > examples/${LATEST_VERSION}/FedRAMP_Moderate-AllowList-SCP.md
aws-allowlister generate -fm --quiet --table > examples/latest/FedRAMP_Moderate-AllowList-SCP.md
# FedRAMP All
aws-allowlister generate -fm -fh --quiet > examples/${LATEST_VERSION}/FedRAMP_All-AllowList-SCP.json
aws-allowlister generate -fm -fh --quiet > examples/latest/FedRAMP_All-AllowList-SCP.json
aws-allowlister generate -fm -fh --quiet --table > examples/${LATEST_VERSION}/FedRAMP_All-AllowList-SCP.md
aws-allowlister generate -fm -fh --quiet --table > examples/latest/FedRAMP_All-AllowList-SCP.md
