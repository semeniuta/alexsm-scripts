#!/bin/sh

REPO_URL=$1
THIS_DIR=$(dirname $0)

LATEST_TAG=$($THIS_DIR/gitlatest.sh $REPO_URL)

CMD="git clone --depth 1 --branch $LATEST_TAG $REPO_URL"

#echo "$CMD"

$CMD

