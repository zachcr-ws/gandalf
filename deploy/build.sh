#!/bin/bash
export GOPATH=/mnt/sdc/gocode
export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin

PROJECT_NAME=gandalf
FULL_PROJECT_NAME=git.curio.im/hacker/gandalf

cd $GOPATH/src/$FULL_PROJECT_NAME

mkdir -p /srv/salt/prod/gandalf/dist/$PROJECT_NAME
rsync -avz --delete ./ /srv/salt/prod/gandalfd/dist/$PROJECT_NAME
