#!/bin/bash

# Usage: integration-test.sh {organization} {project} {path-to-clone}
# Example usage:
#   $ integration-test.sh openstack barbican
#   $ integration-test.sh openstack keystone
#   $ integration-test.sh openstack keystonemiddleware
#   $ integration-test.sh openstack sahara
#   $ integration-test.sh openstack python-keystoneclient \
#       /opt/openstack/python-keystoneclient
set -x
set -e

REPO_ROOT=${REPO_ROOT:-git://git.openstack.org}
org=$1
project=$2

if [[ $# -eq 3 ]] ; then
    projectdir=$3
    clone=0
else
    projectdir=$project
    clone=1
fi

workdir="$(pwd)"

if [[ $clone -eq 1 ]] ; then
    tempdir="$(mktemp -d)"
    trap "rm -rf $tempdir" EXIT

    pushd $tempdir
    git clone $REPO_ROOT/$org/$project --depth=1
fi

pushd $project
    set +e
    # --notest allows us to create the tox-managed virtualenv without
    # running any tests.
    tox -e bandit --notest
    # We then install our local version of bandit into the virtualenv
    .tox/bandit/bin/pip install --force-reinstall -U $workdir
    # And now we actually run the tests
    tox -e bandit
popd

if [[ $clone -eq 1 ]] ; then
    popd
fi
