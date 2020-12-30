#!/bin/sh

REPO_URL=$1

git ls-remote --tags $REPO_URL | cut -f2 | sort | tail -n 1