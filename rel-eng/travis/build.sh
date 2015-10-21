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
travis_home=$HOME/build/$TRAVIS_REPO_SLUG
docker exec -i test_fedora bash -c "export travis_home=$HOME/build/$TRAVIS_REPO_SLUG"
# process package
echo "Building $package_basename"
if [ "$TRAVIS_PULL_REQUEST" == "false" ] ; then
    docker exec -i test_fedora bash -c "export travis_home=$HOME/build/$TRAVIS_REPO_SLUG; 
    python $travis_home/rel-eng/travis/upload.py $COPR_LOGIN nightly $COPR_TOKEN $travis_home/*.src.rpm rpg" >copr.sh 2>coprerr.out &
    copr_pid=$!
else
    LOGIN=Y29wcg==##pcpfxijfcfrjxinpvxrn
    TOKEN=wqzowgqlhelyuoxbplthrbrvqvcroq
    docker exec -i test_fedora bash -c "export travis_home=$HOME/build/$TRAVIS_REPO_SLUG; 
    python $travis_home/rel-eng/travis/upload.py $LOGIN rpgtest $TOKEN $travis_home/*.src.rpm rpg-pull-requests" >copr.sh 2>coprerr.out &
    copr_pid=$!
fi
secs=0
while ps -p $copr_pid > /dev/null; do
    sleep 1
    printf "\r>>> Copr is working -- %02d:%02d <<<" $((++secs/60)) $((secs%60))
done
printf "\r"
wait $copr_pid
STATUS_ALL=$((STATUS_ALL+$?))
cat coprerr.out
sh copr.sh
STATUS_ALL=$((STATUS_ALL+$?))
PATHS='$PATH'
docker exec -i test_fedora bash -c "chown -R fedora:root /tmp /var/tmp $travis_home"
docker exec -i -u fedora test_fedora bash -c "cd $travis_home; export PATH=/usr/bin:$PATHS; 
nosetests-3.4 tests/*/ --with-coverage --cover-package=rpg -v" >../temp.docker_out 2>&1 &
docker_pid=$!
secs=0
while ps -p $docker_pid > /dev/null; do
    sleep 1
    printf "\r>>> Nosetests-3.4 is working -- %02d:%02d <<<" $((++secs/60)) $((secs%60))
done
printf "\r"
wait $docker_pid
status=$?
echo -en "travis_fold:start:$package_basename-test\\r"
if [ $status == 0 ] ; then
    echo "All-Test $(tput setaf 2)succeeded $(tput sgr0)"
else
    echo "All-Test $(tput setaf 1)failed$(tput sgr0)"
fi
cat ../temp.docker_out
echo -en "travis_fold:end:$package_basename-test\\r"
STATUS_ALL=$((STATUS_ALL+status))
echo -en "travis_fold:start:flake8\\r"
if [ "$TRAVIS_PULL_REQUEST" == "false" ] ; then
    docker exec -i test_fedora bash -c "flake8 $travis_home" >../flake8.out
    FLAKE="flake8"
    count=$(cat ../flake8.out | wc -l )
else
    docker exec -i test_fedora bash -c "cd $travis_home; flake8-diff" >../flake8.out
    FLAKE="flake8-diff"
    count=$(($(cat ../flake8.out | wc -l )-$(grep "Found violations:" ../flake8.out | wc -l)))
    STATUS_ALL=$((STATUS_ALL+count))
fi

if [ $count == 0 ] ; then
    echo "$FLAKE $(tput setaf 2)0 $(tput sgr0)error/warning"
else
    echo "$FLAKE $(tput setaf 1)$count $(tput sgr0)error(s)/warning(s)"
fi
cat ../flake8.out
echo -en "travis_fold:end:flake8\\r"
sudo chown -R travis:travis $HOME/build/$TRAVIS_REPO_SLUG
coveralls
docker stop test_fedora >/dev/null && docker rm test_fedora >/dev/null
exit $STATUS_ALL
