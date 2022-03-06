#!/bin/sh

aptitude show $1 | grep Depends: | sed 's/Depends://g' | tr -d ' ' | sed 's/,/\n/g'
