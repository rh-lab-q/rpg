#!/usr/bin/env bash

if [ "$TRAVIS_PULL_REQUEST" == "false" ] ; then
    if [ "$TRAVIS_REPO_SLUG" != "rh-lab-q/rpg" ] ; then
        echo "Permission denied to upload srpm package!"
        exit 0
    fi
    echo -e "Starting to upload srpm package.\n"
    cd $HOME
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis"
    git clone --quiet --branch=srpm https://${GIT_TOKEN}@github.com/PavolVican/rpg.git build_rpm
    cd build_rpm
    package_name=$(ls /tmp/tito/*.src.rpm) #name RPM package
    cp "$package_name" .
    package_name=$(basename "$package_name") 
    message='new srpm from '`echo $package_name | sed 's/.*\(.\{7\}\).src.rpm/\1/'`
    #add, commit and push files
    git add "$package_name"
    git commit "$package_name" -m "$message"
    git push -fq origin srpm > /dev/null
    if [ $? -eq 0 ]; then
        echo -e "Successed upload srpm package!\n"
        cd $HOME/build
        cd $TRAVIS_REPO_SLUG
        python rel-eng/travis/upload.py $COPR_LOGIN $COPR_TOKEN $package_name
    else
        echo -e "Failed upload srpm package!\n"
        exit 1
    fi
fi
exit 0
