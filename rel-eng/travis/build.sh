#!/usr/bin/env bash

STATUS_ALL=0

GITROOT=$(pwd)$(git rev-parse --show-cdup)

echo "$GITROOT"

# For pull requests just compare target branch and github merge commit,
# TRAVIS_COMMIT_RANGE is unusable because there is commit from master
# and if pull request modifies old version, range is big and many files
# differ (may be bug in travis)
if [ "$TRAVIS_PULL_REQUEST" == "false" ] ; then
    COMMIT_RANGE=$TRAVIS_COMMIT_RANGE
else
    COMMIT_RANGE=$TRAVIS_BRANCH...FETCH_HEAD
    git rebase origin/master >/dev/null
    if [ $? -eq 1 ]; then
        echo "Failed to rebase!"
        exit 1
    fi
fi

echo "Commit range: $COMMIT_RANGE"

# our package RPG
package="rpg"
package_basename=$(basename $package)
# process package
echo -en "travis_fold:start:$package_basename-build\\r"
echo "Building $package_basename"
srpm=$(tito build --srpm --test)
tito_ret=$?
srpm=$(echo "$srpm" | awk 'NF{p=$0}END{print p}' | sed 's/^Wrote: //g')
if [ $tito_ret -ne 0 ]; then
    echo "Tito failed to create SRPM"
    exit $tito_ret
fi
echo "SRPM created: $srpm"
echo -en "travis_fold:start:$package_basename-mock\\r"
echo "Running mock"
# build SRPM
sudo mock -r rpg --resultdir=/tmp/mock/$package_basename --arch=noarch --rebuild $srpm >temp.mock_out 2>&1 &
mock_pid=$!
secs=0
while ps -p $mock_pid > /dev/null; do
    sleep 1
    printf "\r>>> Mock is working -- %02d:%02d <<<" $((secs++/60)) $((secs%60))
done
printf "\r"
wait $mock_pid
status=$?
cat temp.mock_out
echo -en "travis_fold:end:$package_basename-mock\\r"
if [ $status -eq 0 ] ; then
    echo "Building $package_basename succeeded"
else
    echo "Mock failed with code: $status"
fi
# output logs
echo -en "travis_fold:start:$package_basename-build-log\\r"
echo "# build.log"
cat /tmp/mock/$package_basename/build.log
echo -en "travis_fold:end:$package_basename-build-log\\r"
echo -en "travis_fold:start:$package_basename-root-log\\r"

echo "# root.log"
cat /tmp/mock/$package_basename/root.log
echo -en "travis_fold:end:$package_basename-root-log\\r"

echo -en "travis_fold:start:$package_basename-state-log\\r"
echo "# state.log"
cat /tmp/mock/$package_basename/state.log
echo -en "travis_fold:end:$package_basename-state-log\\r"

STATUS_ALL=$((STATUS_ALL+status))
echo -en "travis_fold:end:$package_basename-build\\r"

if [ "$TRAVIS_PULL_REQUEST" == "false" ] ; then
    echo -en "travis_fold:start:flake8\\r"
    echo "flake8"
    flake8 .
    echo -en "travis_fold:end:flake8\\r"
else
    echo -en "travis_fold:start:flake8-diff\\r"
    echo "flake8-diff"
    flake8-diff
    echo -en "travis_fold:end:flake8-diff\\r"
fi

exit $STATUS_ALL