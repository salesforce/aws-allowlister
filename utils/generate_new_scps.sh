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
export SCP_FILE_NAME="All-AllowList-SCP"
aws-allowlister generate --quiet > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.json
aws-allowlister generate --quiet > examples/latest/${SCP_FILE_NAME}.json
aws-allowlister generate --quiet --table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.md
aws-allowlister generate --quiet --table > examples/latest/${SCP_FILE_NAME}.md
aws-allowlister generate --quiet --excluded-table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}-Excluded.md
aws-allowlister generate --quiet --excluded-table > examples/latest/${SCP_FILE_NAME}-Excluded.md
# All Commercial (does not include FedRAMP)
export SCP_FILE_NAME="Commercial-AllowList-SCP"
export COMPLIANCE_ARGS="-sphi"
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/latest/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/latest/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}-Excluded.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/latest/${SCP_FILE_NAME}-Excluded.md
# SOC
export SCP_FILE_NAME="SOC-AllowList-SCP"
export COMPLIANCE_ARGS="-s"
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/latest/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/latest/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}-Excluded.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/latest/${SCP_FILE_NAME}-Excluded.md
# PCI
export SCP_FILE_NAME="PCI-AllowList-SCP"
export COMPLIANCE_ARGS="-p"
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/latest/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/latest/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}-Excluded.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/latest/${SCP_FILE_NAME}-Excluded.md
# HIPAA
export SCP_FILE_NAME="HIPAA-AllowList-SCP"
export COMPLIANCE_ARGS="-h"
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/latest/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/latest/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}-Excluded.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/latest/${SCP_FILE_NAME}-Excluded.md
# ISO
export SCP_FILE_NAME="ISO-AllowList-SCP"
export COMPLIANCE_ARGS="-i"
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/latest/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/latest/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}-Excluded.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/latest/${SCP_FILE_NAME}-Excluded.md
# FedRAMP High
export SCP_FILE_NAME="FedRAMP_High-AllowList-SCP"
export COMPLIANCE_ARGS="-fh"
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/latest/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/latest/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}-Excluded.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/latest/${SCP_FILE_NAME}-Excluded.md
# FedRAMP Moderate
export SCP_FILE_NAME="FedRAMP_Moderate-AllowList-SCP"
export COMPLIANCE_ARGS="-fm"
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/latest/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/latest/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}-Excluded.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/latest/${SCP_FILE_NAME}-Excluded.md
# FedRAMP All
export SCP_FILE_NAME="FedRAMP_All-AllowList-SCP"
export COMPLIANCE_ARGS="-fm -fh"
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/latest/${SCP_FILE_NAME}.json
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/latest/${SCP_FILE_NAME}.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}-Excluded.md
aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/latest/${SCP_FILE_NAME}-Excluded.md