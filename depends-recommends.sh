#!/bin/sh

aptitude show $1 | grep -E "Depends:|Recommends:" | sed 's/Depends://' | sed 's/Recommends://' | tr -d ' ' | sed 's/,/\n/g'