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
DIRECTORY=`dirname "$0"`
jq -c '.[]' "$DIRECTORY/config.json" | while read i; do
    SCP_FILE_NAME=$(echo $i | jq -r '.SCP_FILE_NAME')
    COMPLIANCE_ARGS=$(echo $i | jq -r '.COMPLIANCE_ARGS')
    echo "examples/$LATEST_VERSION/${SCP_FILE_NAME}"
    aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.json
    aws-allowlister generate ${COMPLIANCE_ARGS} --quiet > examples/latest/${SCP_FILE_NAME}.json
    aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}.md
    aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --table > examples/latest/${SCP_FILE_NAME}.md
    aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/${LATEST_VERSION}/${SCP_FILE_NAME}-Excluded.md
    aws-allowlister generate ${COMPLIANCE_ARGS} --quiet --excluded-table > examples/latest/${SCP_FILE_NAME}-Excluded.md
done