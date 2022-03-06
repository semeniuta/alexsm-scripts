#!/bin/sh

apt-cache rdepends --installed $1 | sed 1,2d | tr -d ' |'
