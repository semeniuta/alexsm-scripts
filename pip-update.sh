#/bin/sh

pip list --outdated --disable-pip-version-check | tail -n +3 | awk '{print $1;}' | tr '\n' ' ' | xargs pip install --upgrade