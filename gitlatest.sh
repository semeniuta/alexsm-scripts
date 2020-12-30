#!/bin/sh

REPO_URL=$1

LAST=$(git ls-remote --tags $REPO_URL | cut -f 2 | sort | tail -n 1)

# take out the first two fields (refs/tags/)
echo $LAST | cut -d "/" -f 3-