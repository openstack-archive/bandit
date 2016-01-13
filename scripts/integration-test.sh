#!/bin/bash

# Usage: integration-test.sh {organization} {project}
# Example usage:
#   $ integration-test.sh openstack barbican
#   $ integration-test.sh openstack keystone
#   $ integration-test.sh openstack keystonemiddleware
#   $ integration-test.sh openstack sahara
# Note: you can clone from a local file with REPO_ROOT=file:////~/path/to/repo
set -x
set -e
REPO_ROOT=${REPO_ROOT:-git://git.openstack.org}
org=$1
project=$2

workdir="$(pwd)"
tempdir="$(mktemp -d)"

pushd $tempdir
    if [[ $REPO_ROOT == file://* ]]; then
        git clone $REPO_ROOT/$org/$project
    else
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
popd

rm -rf $tempdir
