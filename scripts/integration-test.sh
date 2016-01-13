#!/bin/bash

# Usage: test.sh openstack keystone
# Note: you can clone from a local file with REPO_ROOT=file:////~/path/to/repo
set -x
set -e
REPO_ROOT=${REPO_ROOT:-git://git.openstack.org}
org=$1
project=$2

if [[ $REPO_ROOT == file://* ]]; then
    git clone $REPO_ROOT/$org/$project
else
    git clone $REPO_ROOT/$org/$project --depth=1
fi

pushd $project
    set +e
    tox -e bandit
popd

rm -rf $project
